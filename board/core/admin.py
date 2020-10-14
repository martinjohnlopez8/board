from django.contrib import admin
from .models import (
	Board,
	Post,
	Thread,
	UserProfile,
)
# Register your models here.
admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Thread)

