import json, re
import statistics

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q, Avg
from django.core.paginator import Paginator

from room.models           import Room, Category, RoomAmenity, Image, Amenity, WishList, DisableDate, AbleTime
from user.models           import Host, Review

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
