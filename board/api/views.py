from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import (
    generics,
    mixins,
    status,
    views
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .permissions import (
    IsAdmin,
    IsAdminOrModerator,
    IsModerator
)
from . import serializers
from core.models import (
    Board,
    Post,
    Thread,
    UserProfile
)

from django_gravatar.helpers import (
    get_gravatar_url, has_gravatar,
    get_gravatar_profile_url,
    calculate_gravatar_hash
)


# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = serializers.UserProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message': 'Success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Error',
                'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        data = serializer.validated_data
        username = data.get('username', None)
        email = data.get('email', None)
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)

        if serializer.is_valid():
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
            )
            send_mail(
                'Confirmation Email',
                'Your email is confirmed',
                None,
                [email],
                fail_silently=False
            )


class LoginView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        phone_number = request.POST.get('phone_number', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user_authenticated = False
        if email:
            try:
                user = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                return Response({
                    'message': 'Incorrect Login Credentials',
                })
            if user:
                user_authenticated = authenticate(email=email, password=password)
        elif phone_number:
            try:
                user = UserProfile.objects.get(phone_number=phone_number).user
            except UserProfile.DoesNotExist:
                return Response({
                    'message': 'Incorrect Login Credentials',
                })
            if user:
                user_authenticated = user.check_password(password)

        if user_authenticated:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
            })

        return Response({
            'message': 'Incorrect Login Credentials',
        })


class FollowUserView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)

        if username:
            user = get_object_or_404(User, username=username)
            if user:
                request.user.profile.follows.add(user)
                return Response({
                    'message': 'Success',
                })

        return Response({
            'message': 'Failed',
        })


class UnfollowUserView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)

        if username:
            user = get_object_or_404(User, username=username)
            if user:
                request.user.profile.follows.remove(user)
                return Response({
                    'message': 'Success',
                })

        return Response({
            'message': 'Failed',
        })


class UserProfileDisplayView(generics.RetrieveAPIView):
    serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        user_id = self.request.user.id
        return UserProfile.objects.get(user__id=user_id)


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserProfileUpdateSerializer

    def get_object(self):
        user_id = self.request.user.id
        return UserProfile.objects.get(user__id=user_id)


class BanUserView(views.APIView):
    permission_classes = [IsAdminOrModerator]

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id', None)
        if user_id:
            user = get_object_or_404(User, id=user_id)
            if user:
                user.profile.is_banned = True
                user.profile.save()
                return Response({
                    'message': 'Success',
                })
        return Response({
            'message': 'Failed',
        })


class UnbanUserView(views.APIView):
    permission_classes = [IsAdminOrModerator]

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id', None)
        if user_id:
            user = get_object_or_404(User, id=user_id)
            if user:
                user.profile.is_banned = False
                user.profile.save()
                return Response({
                    'message': 'Success',
                })
        return Response({
            'message': 'Failed',
        })


class LockUnlockThread(views.APIView):
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        thread_id = request.POST.get('thread_id', None)
        if thread_id:
            thread = get_object_or_404(Thread, id=thread_id)
            if thread:
                if thread.is_locked:
                    thread.is_locked = False
                else:
                    thread.is_locked = True
                thread.save()
                return Response({
                    'message': 'Success',
                })

        return Response({
            'message': 'Failed',
        })


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminOrModerator]
    serializer_class = serializers.BoardSerializer


class ThreadCreateView(generics.CreateAPIView):
    serializer_class = serializers.ThreadSerializer


class PostCreateView(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer


class BoardListView(generics.ListAPIView):
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        boards = Board.objects.filter(
            thread__isnull=False, thread__post__isnull=False
        )
        return boards


class UserPostListView(generics.ListAPIView):
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        return Post.objects.filter(user__id=user_id)


class UserGravatarView(views.APIView):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        if email:
            gravatar_exists = has_gravatar(email)
            if gravatar_exists:
                return Response({
                    'url': get_gravatar_url(email),
                })
        return Response({
            'message': 'Gravatar does not exist',
        })

