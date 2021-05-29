import json, re, bcrypt, jwt

from datetime               import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models       import Avg
from django.http            import JsonResponse
from django.views           import View
from room.models            import Room, Category, RoomAmenity,Image,Amenity,WishList,DisableDate,AbleTime
from user.models            import User, Host, Review
from user.utils             import LoginRequired

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
