"""Django built-in admin site (/django-admin/) setup for users. Super Admin only."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active", "last_login")
    list_filter = ("role", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Hospital", {"fields": ("role", "phone", "can_archive_patients", "can_manage_admissions", "created_by")}),
    )
