from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=128, unique=True, null=True)
    first_name   = models.CharField(max_length=32, null=True)
    last_name    = models.CharField(max_length=32, null=True)
    password     = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=32, unique=True, null=True)
    birthday     = models.CharField(max_length=32, null=True)
    sex          = models.CharField(max_length=32, null=True)
    create_at    = models.DateTimeField(auto_now_add=True)
    update_at    = models.DateTimeField(auto_now=True)
    profile_url  = models.CharField(max_length=2000, null=True)
    review       = models.ManyToManyField("User", through="Review", related_name="user")
    wishlist     = models.ManyToManyField("room.Room", through="room.WishList", related_name="user")

    class Meta:
        db_table = "users"

class Review(models.Model):
    review_user       = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_review")
    review_room       = models.ForeignKey("room.Room", on_delete=models.CASCADE, related_name="room_review")
    comment           = models.TextField(null=True)
    cleanliness       = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=None)
    communication     = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=None)
    checkin           = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=None)
    accuracy          = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=None)
    location          = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=None)
    cost_effectivenes = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=None)

    class Meta:
        db_table = "reviews"

class Host(models.Model):
    user     = models.ForeignKey("User", on_delete=models.CASCADE, related_name="host")
    is_super = models.BooleanField(default=False)

    class Meta:
        db_table = "hosts"