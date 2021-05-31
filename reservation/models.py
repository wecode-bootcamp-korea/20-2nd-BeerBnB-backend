from django.db import models

class Reservation(models.Model):
    checkin  = models.DateField()
    checkout = models.DateField()
    status   = models.ForeignKey("Status", on_delete=models.CASCADE)
    user     = models.ForeignKey("user.User", on_delete=models.CASCADE)
    room     = models.ForeignKey("room.Room", on_delete=models.CASCADE)

    class Meta:
        db_table = "reservations"

class Status(models.Model):
    status = models.CharField(max_length=128)

    class Meta:
        db_table = "status"