from django.contrib.auth.models import User
from rest_framework import serializers

from car_parking.models import ParkingSpot, ParkingReservation
from phonenumber_field import serializerfields


class UserRegistrationSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.EmailField(required=False)
    phone_number = serializerfields.PhoneNumberField(required=False)

    class Meta:
        fields = ['password', 'phone_number', 'email']

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        email = attrs.get('email')

        if not phone_number and not email:
            raise serializers.ValidationError("At least one of phone_number or email must be provided.")

        if phone_number and email:
            raise serializers.ValidationError("Can not provide both phone number and Email ")

        return attrs


class ParkingSpotSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    def get_longitude(self, obj):
        return obj.location.x if obj.location else None

    class Meta:
        model = ParkingSpot
        fields = ["id", "latitude", "longitude", "per_hour_rate"]


class ReserveParkingSpotInput(serializers.Serializer):
    parking_spot_id = serializers.IntegerField()
    hours = serializers.IntegerField()

    class Meta:
        fields = ['parking_spot_id', 'hours']


class ParkingReservationSerializer(serializers.ModelSerializer):
    parking_spot = ParkingSpotSerializer()

    class Meta:
        model = ParkingReservation
        fields = ['created_at', 'reserve_for_hours', "parking_spot"]
