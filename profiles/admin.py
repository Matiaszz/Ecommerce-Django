"""Admin profiles"""
from django.contrib import admin
from .models import ProfileUser


@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    """Profile user admin"""
