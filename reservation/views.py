import json

from django.http        import JsonResponse
from django.views       import View

from reservation.models import Reservation, Status
from reservation.check  import check
from room.models        import Room,AbleTime
from user.utils         import LoginRequired

class ReservationView(View):
    @LoginRequired
    def post(self, request):
        try:
            data        = json.loads(request.body)
            room        = Room.objects.get(name=data['room'])
            reservation = Status.objects.get(status="reservation")
            checkin     = data['checkin']
            checkout    = data['checkout']
            adult       = int(data['adult'])
            child       = int(data['child'])

            if room.capacity < adult + child:
                return JsonResponse({'MESSAGE':'Max capacity is overed'}, status=400)

            if not check(room, checkin, checkout):
                return JsonResponse({'MESSAGE':'not_available_date'}, status=400)

            reservation = Reservation.objects.create(
                room     = room,
                user     = request.user,
                checkin  = checkin,
                checkout = checkout,
                status   = reservation
            ) 

            return JsonResponse({'MESSAGE':'reservation success'}, status=200)
        except KeyError:
            return JsonResponse({'message':'key error'}, status=404)

        except Room.DoesNotExist:
            return JsonResponse({'MESSAGE':'roomname_not_available'}, status=400)
