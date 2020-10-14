from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.DO_NOTHING)
    about_myself = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    hometown = models.CharField(max_length=150, blank=True)
    present_location = models.CharField(max_length=150, blank=True, null=True)
    geolocation = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, unique=True)
    is_banned = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    follows = models.ManyToManyField(User, related_name='followed_by')

    @property
    def followed_by(self):
        if self.user:
            return self.user.followed_by.all().values_list('user__username')
        return


class Board(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_draft = models.BooleanField(default=False)

    @property
    def thread_count(self):
        return self.thread.all().count()

    @property
    def post_count(self):
        return Post.objects.filter(thread__board=self).count()


class Thread(models.Model):
    name = models.CharField(max_length=150, null=True, unique=True)
    last_reply_date = models.DateTimeField(null=True)
    last_poster = models.CharField(max_length=100, null=True)
    is_locked = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='thread')
    is_draft = models.BooleanField(default=False)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post', null=True)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, related_name='post')
    is_draft = models.BooleanField(default=False)

    @property
    def publisher_name(self):
        if self.user:
            return self.user.username
        return None
