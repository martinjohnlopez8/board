from rest_framework import serializers
from core.models import (
    Board,
    Post,
    Thread,
    UserProfile
)


class UserProfileCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'password', 'phone_number', 'username']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['about_myself', 'date_of_birth', 'hometown',
                  'present_location', 'geolocation', 'follows',
                  'followed_by']


class UserProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['about_myself', 'date_of_birth', 'hometown',
                  'present_location', 'geolocation']


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ['name', 'description', 'is_draft']


class ThreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ['name', 'board', 'is_draft']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content', 'thread', 'is_draft']
