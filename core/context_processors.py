"""Runs on every page: provides hospital branding and the bell-menu notifications to all templates."""
from .constants import NOTIFICATION_COUNT
from .models import ActivityLog, SystemSetting


def hospital(request):
    """Makes hospital branding and the notification feed available in every template."""
    context = {"hospital": SystemSetting.load()}
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        logs = ActivityLog.objects.select_related("user")
        if not user.is_super_admin:
            logs = logs.filter(user=user)
        context["nav_notifications"] = list(logs[:NOTIFICATION_COUNT])
    return context
