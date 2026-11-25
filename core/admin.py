"""Django built-in admin registration for settings and activity logs."""
from django.contrib import admin

from .models import ActivityLog, SystemSetting

admin.site.register(SystemSetting)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "action", "description", "ip_address")
    list_filter = ("action",)
    search_fields = ("description", "user__username")
