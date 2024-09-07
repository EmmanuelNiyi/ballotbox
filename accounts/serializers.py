from datetime import datetime

from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer, Serializer

from accounts.models import Role, UserActivation, User, UserProfile


# User = settings.AUTH_USER_MODEL


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'roles', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        # extra_kwargs = {'password': {'write_only': True}}


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['last_name']


class UserActivationSerializer(Serializer):
    user_email = EmailField()
    activation_key = serializers.CharField(write_only=True, required=False)

    class Meta:
        fields = ['user_email', 'activation_key']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class TailoredUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'date_of_birth', 'level']

