import random

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import logging

from accounts.models import Role, User, UserActivation, UserProfile
from accounts.serializers import RoleSerializer, UserSerializer, UserActivationSerializer, LoginSerializer, \
    UserProfileSerializer, TailoredUserProfileSerializer
from accounts.utilities.activation import send_email, generate_activation

# Create your views here.

logger = logging.getLogger(__name__)


class CreateRoleView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class GetAllRolesView(ListAPIView):
    """Get all roles view"""

    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                serializer.validated_data['is_active'] = False
                serializer.validated_data['is_staff'] = False
                activation_key = generate_activation()
                serializer.save()
                activate = UserActivation.objects.create(user_id=serializer.data['id'], activation_key=activation_key)
                activate.save()
                send_email(serializer.data['email'], activation_key)
                serializer.validated_data['password'] = ''
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating user: {e}")
                return Response({"error": "Error creating user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Invalid data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserAccountDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get_object(self):
        return self.request.user


class SendActivationCodeView(generics.CreateAPIView):
    serializer_class = UserActivationSerializer
    queryset = UserActivation.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['user_email']
            try:
                user = User.objects.filter(email=user_email)[0]
                user = User.objects.get(id=user.id)
            except User.DoesNotExist:
                return Response("User not found", status=status.HTTP_404_NOT_FOUND)

            activation_key = generate_activation()
            activate, _created = UserActivation.objects.update_or_create(
                user_id=user.id,
                defaults={'activation_key': activation_key}
            )

            try:
                activate.save()
            except Exception as e:
                return Response(f"Error saving activation: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            result = send_email(user.email, activation_key)

            if result:
                return Response('Activation code sent', status=status.HTTP_200_OK)
            else:
                return Response('Error sending activation code', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(generics.RetrieveAPIView):
    serializer_class = UserActivationSerializer
    queryset = UserActivation.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data['user_email'])[0]
            real_code = UserActivation.objects.filter(user_id=user.id,
                                                      activation_key=serializer.validated_data['activation_key'])
            if real_code:
                user.is_active = True
                user.save()
                return Response('Activation successful', status=status.HTTP_200_OK)
            return Response('Activation Failed, check your code', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        # Retrieve username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # If user is active, create a user serializer instance
                user_serializer = UserSerializer(user)

                # Generate tokens using RefreshToken
                refresh = RefreshToken.for_user(user)

                # Prepare response data
                response_data = {
                    'user': user_serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # User is not active
                return Response('User account is disabled.', status=status.HTTP_400_BAD_REQUEST)
        else:
            # Authentication failed
            return Response('Wrong username or password', status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TailoredUserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'user'


class GetAllUserProfilesView(ListAPIView):
    """Get all User Profiles view"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
