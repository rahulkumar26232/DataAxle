from django.urls import path

from car_parking.apis.parking_spot import ParkingSpotFetchApi, ReserveParkingSpotApi, ReservedParkingHistoryApi
from car_parking.apis.signup import UserSignupApi, UserSignInApi

urlpatterns = [
    path('signup/', UserSignupApi.as_view()),
    path('signin/', UserSignInApi.as_view()),
    path('parking-spot/fetch/', ParkingSpotFetchApi.as_view({'get': 'list'})),
    path('parking-spot/reserve/', ReserveParkingSpotApi.as_view()),
    path('parking-spot/reserved/list/', ReservedParkingHistoryApi.as_view({'get': 'list'})),
]
