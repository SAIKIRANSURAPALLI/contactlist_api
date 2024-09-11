from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.conf import settings
import jwt
import datetime

class RegisterView(GenericAPIView):
    serializer_class = UserSerializer  
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            response_data = {
                'user': UserSerializer(user).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get('username')
            password = data.get('password')

            user = auth.authenticate(username=username, password=password)

            if user:
                auth_token = jwt.encode(
                    {
                        'username': user.username,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) 
                    }, 
                    settings.JWT_SECRET_KEY,
                    algorithm='HS256'
                )
                user_serializer = UserSerializer(user)
                response_data = {
                    'user': user_serializer.data,
                    'token': auth_token
                }
                return Response(response_data, status=status.HTTP_200_OK)
            
            return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
