from django.contrib import admin
from .models import User, Profile, Post, Follower, Following
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Following)
