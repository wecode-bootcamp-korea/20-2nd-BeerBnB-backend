from datetime           import datetime,date
from dateutil.parser    import parse
from reservation.models import Reservation,Status

def check(room, checkin, checkout):
    reservation  = Status.objects.get(status="reservation")
    reservations = Reservation.objects.filter(room=room, status=reservation)
    checkin      = parse(checkin).date()
    checkout     = parse(checkout).date()

    if not reservations:
        return True

    if not (room.disable_date.start_date > checkout or room.disable_date.end_date < checkin):
        return False

    for reservation in reservations:
        if reservation.checkin < checkout and reservation.checkout > checkin:
            return False
    return True

def check_in(room, checkin):
    reservation  = Status.objects.get(status="reservation")
    reservations = Reservation.objects.filter(room=room, status=reservation)
    checkin      = parse(checkin).date()

    if not reservations:
        return True

    if not (room.disable_date.start_date > checkin or room.disable_date.end_date < checkin):
        return False

    for reservation in reservations:
        if not(reservation.checkin > checkin or reservation.checkout <= checkin):
            return False
    return True

def check_out(room, checkout):
    reservation  = Status.objects.get(status="reservation")
    reservations = Reservation.objects.filter(room=room, status=reservation)
    checkout     = parse(checkout).date()

    if not reservations:
        return True

    if not (room.disable_date.start_date > checkout or room.disable_date.end_date < checkout):
        return False
    for reservation in reservations:
        if not(reservation.checkin >= checkout or reservation.checkout < checkout):
            return False
    return True
