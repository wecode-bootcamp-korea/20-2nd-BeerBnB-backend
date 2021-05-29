from datetime           import datetime,date
from dateutil.parser    import parse
from reservation.models import Reservation,Status

def check(room, checkin, checkout):
    reservation  = Status.objects.get(status="reservation")
    reservations = Reservation.objects.filter(room=room, status=reservation)
    checkin      = parse(checkin).date()
    checkout     = parse(checkout).date()

    if not reservations:
        return False

    if not (room.disable_date.start_date > checkout or room.disable_date.end_date < checkin):
        return False

    for reservation in reservations:
        if reservation.checkin < checkout and reservation.checkout > checkin:
            return False
    return True
