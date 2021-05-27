import datetime
from django.db import models

class Room(models.Model):
    name         = models.CharField(max_length=128)
    min_date     = models.CharField(max_length=32, default="1")
    city         = models.CharField(max_length=128)
    capacity     = models.IntegerField()
    latitude     = models.DecimalField(max_digits=9, decimal_places=7)
    longtitude   = models.DecimalField(max_digits=10, decimal_places=7)
    is_refund    = models.BooleanField(default=False)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    host         = models.ForeignKey("user.Host", on_delete=models.CASCADE, related_name="room")
    category     = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="room")
    able_time    = models.ForeignKey("AbleTime", on_delete=models.CASCADE, related_name="room")
    disable_date = models.ForeignKey("DisableDate", on_delete=models.CASCADE, related_name="room", null=True)
    amenity      = models.ManyToManyField("Amenity", through="RoomAmenity", related_name="room")

    class Meta:
        db_table = "rooms"

class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "categories"
        
class RoomAmenity(models.Model):
    room    = models.ForeignKey("Room", on_delete=models.CASCADE)
    amenity = models.ForeignKey("Amenity", on_delete=models.CASCADE)

    class Meta:
        db_table = "room_amenities"

class Image(models.Model):
    url  = models.CharField(max_length=2000)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="image")

    class Meta:
        db_table = "images"

class Amenity(models.Model):
    name  = models.CharField(max_length=128)
    image = models.CharField(max_length=2000)

    class Meta:
        db_table = "amenities"

class WishList(models.Model):
    wish_user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="user_wish")
    wish_room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="room_wish")

    class Meta:
        db_table = "wishlists"

class DisableDate(models.Model):
    start_date = models.DateField(null=True)
    end_date   = models.DateField(null=True)

    class Meta:
        db_table = "disable_dates"

class AbleTime(models.Model):
    checkin  = models.TimeField(default=datetime.time(15))
    checkout = models.TimeField(default=datetime.time(11))

    class Meta:
        db_table = "able_times"