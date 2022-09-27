from django.contrib import admin
from .models import User, Post

from django.urls import reverse
from django.utils.http import urlencode

@admin.register(User)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "link")
    list_display_links = ('link',)

