from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from car_parking.models import ParkingSpot, ParkingReservation
from car_parking.serializer import ParkingSpotSerializer, ReserveParkingSpotInput, ParkingReservationSerializer


class ParkingSpotFetchApi(ListModelMixin,viewsets.GenericViewSet):
    serializer_class = ParkingSpotSerializer

    def get_queryset(self):
        latitude = self.request.query_params.get("latitude")
        longitude = self.request.query_params.get("longitude")
        radius = self.request.query_params.get("radius")

        spots = ParkingSpot.objects.filter(is_available=True)

        if latitude and longitude and radius:
            user_location = Point(float(longitude), float(latitude), srid=4326)
            spots = spots.filter(location__distance_lte=(user_location, Distance(m=radius)))

        return spots


class ReserveParkingSpotApi(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = ReserveParkingSpotInput(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        parking_spot_id = request.data.get('parking_spot_id', None)
        hours = request.data['hours']
        user_id= request.user.id

        try:
            spot = ParkingSpot.objects.get(id=parking_spot_id,is_available=True)
        except ParkingSpot.DoesNotExist:
            return Response({
            'status': 'failure', 'message': 'parking spot is not available'
            , "payload": {}
        })

        spot.is_available=False
        spot.save()

        ParkingReservation.objects.create(user_id=user_id,parking_spot_id=spot.id,reserve_for_hours=hours)


        return Response({
            'status': 'success', 'message': 'spot reserved successfully'
            , "payload": {'price': spot.per_hour_rate*hours}
        })


class ReservedParkingHistoryApi(ListModelMixin,viewsets.GenericViewSet):
    serializer_class = ParkingReservationSerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return ParkingReservation.objects.filter(user_id=self.request.user.pk).select_related("parking_spot")
