from rest_framework import serializers
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65,
        min_length=8,
        write_only=True
    )
    email = serializers.EmailField(
        max_length=255,
        min_length=4,
        required=False
    )
    username = serializers.CharField(
        max_length=255,
        min_length=4,
        required=True
    )
    phone_number = serializers.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        max_length=15,
        min_length=4,
        required=True,
        error_messages={
            'invalid': 'Enter a valid phone number.',
        }
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password')

    def validate(self, attrs):
        if CustomUser.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({'phone_number': 'Phone number already exists'})
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email', '')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=email,
            phone_number=validated_data['phone_number']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=255,
        min_length=4,
        required=True
    )
    password = serializers.CharField(
        max_length=65,
        min_length=8,
        write_only=True
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        
        attrs['user'] = user
        return attrs
