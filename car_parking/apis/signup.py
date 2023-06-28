from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from car_parking.models import User
from car_parking.serializer import UserRegistrationSerializer
from car_parking.services import authenticate


class UserSignupApi(APIView):

    @transaction.atomic
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email', None)
        password = request.data['password']
        phone_number = request.data.get('phone_number', None)

        try:
            user = User(email=email, phone_number=phone_number)
            user.password = make_password(password)
            user.save()
        except IntegrityError:
            return Response({'status': 'failure', 'message': 'User Already exists', "payload": {}})

        token = Token.objects.create(user=user)

        return Response({
            'status': 'success', 'message': 'User successfully signed up'
            , "payload": {'access_token': token.key}
        })


class UserSignInApi(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email', None)
        password = request.data['password']
        phone_number = request.data.get('email', None)

        username = email if email else phone_number

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)

            return JsonResponse({
                'status': 'success', 'message': 'User successfully signed IN'
                , "payload": {'access_token': token.key}
            })

        return JsonResponse({
            'status': 'failire', 'message': 'Invalid username or password'
            , "payload": {}
        })
