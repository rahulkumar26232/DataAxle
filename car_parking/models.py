from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from phonenumber_field import modelfields
from django.contrib.gis.db import models as point_model


class User(AbstractUser):
    phone_number = modelfields.PhoneNumberField(unique=True,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)

    REQUIRED_FIELDS = []

    class Meta:
        swappable = "AUTH_USER_MODEL"
        constraints = [
            models.CheckConstraint(
                check=Q(phone_number__isnull=False) | Q(email__isnull=False),
                name='not_both_null'
            )
        ]


class ParkingSpot(models.Model):
    location = point_model.PointField()
    per_hour_rate = models.DecimalField(decimal_places=2,max_digits=4)
    is_available = models.BooleanField(default=True)


class ParkingReservation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSpot,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reserve_for_hours = models.IntegerField()
