"""Accounts serializers."""

# Django
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator, FileExtensionValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name', 'last_name', 'is_superuser')

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'phone_number',
            'name',
            'last_name',
            'id',
        )

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField();
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['phone_number'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError('Email or Password Invalid')
        
        self.context['user'] = user
        return data

    def create(self, data):
        return self.context['user']

class UserSignUpSerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Debes introducir un número con el siguiente formato: +999999999. El límite son de 15 dígitos."
    )
    
    phone_number = serializers.CharField(validators=[phone_regex], required=False)

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=100)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords do not match")
        
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        print(data)
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        authenticate(username=user.phone_number, password=user.password)
        return user