import json, re, bcrypt, jwt

from datetime               import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models       import Avg
from django.http            import JsonResponse
from django.views           import View
from room.models            import Room, Category, RoomAmenity,Image,Amenity,WishList,DisableDate,AbleTime
from reservation.check      import check, check_in, check_out
from user.models            import User, Host, Review
from user.utils             import LoginRequired

class RoomListView(View):
    def get(self,request):
        try: 
            city       = request.GET.get('city','')
            checkin    = request.GET.get('checkin',None)
            checkout   = request.GET.get('checkout', None)
            adult      = int(request.GET.get('adult','0'))
            child      = int(request.GET.get('child','0'))
            min_price  = request.GET.get('min_price',0)
            max_price  = request.GET.get('max_price',100000000)
            is_refund  = True if request.GET.get('is_refund',None) == 'true' else False
            is_super   = True if request.GET.get('is_super',None) == 'true' else False
            room_types = request.GET.getlist('room_type',None)
            amenities  = request.GET.getlist('amenity',None)
            page       = int(request.GET.get('page', '1'))
            
            #필터
            list_criteria = {
                    'city__contains': city,
                    'price__range'  : [min_price,max_price],
                    'capacity__gte' : adult+child
                    }
            if room_types: 
                list_criteria['category__name__in'] = room_types
            if amenities: 
                list_criteria['amenity__name__in']  = amenities
            if is_super: 
                list_criteria['host__is_super']     = is_super
            if is_refund: 
                list_criteria['is_refund']          = is_refund

            #paginator
            size   = 10
            offset = (page-1) * size
            limit  = page * size

            room_list = Room.objects.filter(**list_criteria)
            
            #날짜 필터
            if checkin and checkout:
                room_list = [room for room in room_list if check(room, checkin, checkout)]
            if checkin:
                room_list = [room for room in room_list if check_in(room, checkin)]
            if checkout:
                room_list = [room for room in room_list if check_out(room, checkout)]
            if not room_list:
                return JsonResponse({'message':'NO_ROOM_AVAILABLE'}, status=400)

            rating_list = [field.name for field in Review._meta.get_fields() if field.name not in ['id','review_user','review_room','comment']]
            
            room_thumbnail = [{
                'room_id'    : room.id,
                'room_name'  : room.name,
                'price'      : room.price,
                'address'    : room.city,
                'room_type'  : room.category.name,
                'lat'        : room.latitude,
                'lng'        : room.longtitude,
                'image'      : [image.url for image in room.image.all()],
                'is_super'   : room.host.is_super,
                'capacity'   : int(room.capacity),
                'amenity'    : [roomamenity.amenity.name for roomamenity in room.roomamenity_set.all()],
                'rating'     : [{
                    'category'       : category,
                    'category_rating': Review.objects.filter(review_room=room).aggregate(rate_avg=Avg(category))['rate_avg']
                } for category in rating_list
                ]
            } for room in room_list[offset:limit]
            ]

            common_data = len(room_list)
                
            return JsonResponse({'thumbnail': room_thumbnail, 'common':common_data }, status=200)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)

class RoomView(View):
    def get(self,request, room_id):
        try: 
            room        = Room.objects.get(id=room_id)
            rating_list = [field.name for field in Review._meta.get_fields() if field.name not in ['id','review_user','review_room','comment']]

            room_detail = {
                'room_name': room.name,
                'address'  : room.city,
                'price'    : room.price,
                'room_type': room.category.name,
                'image'    : [image.url for image in room.image.all()][0],
                'is_super' : room.host.is_super,
                'host'     : room.host.user.last_name + room.host.user.first_name,
                'capacity' : room.capacity,
                'amenity'  : [{
                    'id'         : roomamenity.amenity.id,
                    'icon'       : re.sub('<i class=\\"|\\"></i>', '',roomamenity.amenity.image),
                    'description': roomamenity.amenity.name
                } for roomamenity in room.roomamenity_set.all()
                ],
                'rating'   : [{
                    'category'       : category,
                    'category_rating': int(Review.objects.filter(review_room=room).aggregate(Avg(category)).get(category+'__avg'))
                } for category in rating_list
                ]
            }
            
            return JsonResponse({'detail': room_detail}, status=200)
       
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
        except Room.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND_ROOM_ID'}, status=400)

class WishListView(View):
    @LoginRequired
    def post(self, request, room_id):
        user = request.user

        try:
            if WishList.objects.filter(wish_user=user, wish_room_id=room_id).exists():
                return JsonResponse({'MESSAGE':'Already Choosen'}, status=400)
            
            WishList.objects.create(
                wish_user_id = 1,
                wish_room_id = room_id
                )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)    

    @LoginRequired
    def delete(self, request, room_id):
        try:
            user = request.user
            wish = WishList.objects.get(wish_user=user, wish_room_id=room_id)
            
            wish.delete()
            return JsonResponse({'MESSAGE':'Delete Success'}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)
        except WishList.DoesNotExist:
            return JsonResponse({'MESSAGE':'Already not Exist in list'}, status=400)

    @LoginRequired
    def get(self, request):
        try:
            user        = request.user
            wishlists   = WishList.objects.filter(wish_user = user)
            rating_list = [field.name for field in Review._meta.get_fields() if field.name not in ['id','review_user','review_room','comment']]

            if not wishlists:
                return JsonResponse({'MESSAGE':'nothing in cart'}, status=400)


            result = [{
                'room_id'  : wishlist.wish_room.id,
                'room_name': wishlist.wish_room.name,
                'address'  : wishlist.wish_room.city,
                'price'    : wishlist.wish_room.price,
                'room_type': wishlist.wish_room.category.name,
                'image'    : [image.url for image in wishlist.wish_room.image.all()],
                'is_super' : wishlist.wish_room.host.is_super,
                'capacity' : wishlist.wish_room.capacity,
                'lat'      : wishlist.wish_room.latitude,
                'lng'      : wishlist.wish_room.longtitude,
                'amenity'  : [roomamenity.amenity.name for roomamenity in wishlist.wish_room.roomamenity_set.all()],
                'rating'   : [{
                    'category'       : category,
                    'category_rating': Review.objects.filter(review_room=wishlist.wish_room).aggregate(Avg(category)).get(category+'__avg')
                } for category in rating_list
                ]
            } for wishlist in wishlists]
            
            return JsonResponse({'result':result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)
