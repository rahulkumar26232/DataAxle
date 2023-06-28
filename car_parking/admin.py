from django.contrib import admin

from car_parking.models import ParkingSpot, ParkingReservation, User

# Register your models here.
admin.site.register(ParkingSpot)
admin.site.register(ParkingReservation)
admin.site.register(User)