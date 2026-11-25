"""System settings page (Super Admin) and the custom 403 / 404 error pages."""
from django.contrib import messages
from django.shortcuts import redirect, render

from .decorators import super_admin_required
from .forms import SystemSettingForm
from .models import ActivityLog, SystemSetting
from .utils import log_activity


@super_admin_required
def system_settings(request):
    """Edit hospital name, Patient ID prefix and rows per page (Super Admin only)."""
    form = SystemSettingForm(request.POST or None, instance=SystemSetting.load())
    if request.method == "POST" and form.is_valid():
        form.save()
        log_activity(request.user, ActivityLog.Action.SETTINGS, "Updated system settings", request)
        messages.success(request, "System settings saved.")
        return redirect("core:settings")
    return render(request, "core/settings.html", {"form": form})


def permission_denied(request, exception=None):
    """Custom 403 page shown when a role is not allowed to open a page."""
    return render(request, "error.html", {
        "code": 403, "title": "Access denied",
        "message": "Your role does not have permission to open this page.",
    }, status=403)


def page_not_found(request, exception=None):
    """Custom 404 page."""
    return render(request, "error.html", {
        "code": 404, "title": "Page not found",
        "message": "The page or record you are looking for does not exist.",
    }, status=404)
