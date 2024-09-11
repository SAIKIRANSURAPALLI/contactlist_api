import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth import get_user_model

class JWTAuthenticationMiddleware(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode('utf-8')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Authorization header must start with Bearer')
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid authorization header format')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            User = get_user_model()  # Use get_user_model() to support custom user models
            user = User.objects.get(username=payload['username'])
            return (user, token)
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Your token is invalid, login again')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Your token has expired, login again')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return None
