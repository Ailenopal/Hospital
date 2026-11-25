"""Home redirect plus the two different dashboards (Super Admin and Admin)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import CustomUser
from admissions.models import Admission
from core.constants import (ADMIN_CHART_DAYS, DASHBOARD_CURRENT_ADMISSIONS, DASHBOARD_RECENT_ACTIVITIES,
                            DASHBOARD_RECENT_ADMINS, DASHBOARD_RECENT_PATIENTS, SUPER_ADMIN_CHART_MONTHS)
from core.decorators import admin_required, super_admin_required
from core.models import ActivityLog
from patients.models import Patient
from reports import services


@login_required
def home(request):
    """Send each role to its own dashboard."""
    if request.user.is_super_admin:
        return redirect("dashboard:super_admin")
    return redirect("dashboard:admin")


@super_admin_required
def super_admin_dashboard(request):
    """Super Admin dashboard: system-wide numbers, charts, admins and all activity."""
    return render(request, "dashboard/super_admin.html", {
        "stats": services.headline_stats(),
        "charts": {
            "monthly": services.registrations_by_month(SUPER_ADMIN_CHART_MONTHS),
            "gender": services.gender_breakdown(),
        },
        "recent_patients": Patient.objects.filter(is_archived=False).select_related("registered_by")[:DASHBOARD_RECENT_PATIENTS],
        "recent_activities": ActivityLog.objects.select_related("user")[:DASHBOARD_RECENT_ACTIVITIES],
        "recent_admins": CustomUser.objects.filter(role=CustomUser.Role.ADMIN).order_by("-created_at")[:DASHBOARD_RECENT_ADMINS],
    })


@admin_required
def admin_dashboard(request):
    """Admin dashboard: patient numbers, charts and the Admin's own recent activity."""
    return render(request, "dashboard/admin.html", {
        "stats": services.headline_stats(),
        "charts": {
            "daily": services.registrations_by_day(ADMIN_CHART_DAYS),
            "status": services.status_breakdown(),
        },
        "recent_patients": Patient.objects.filter(is_archived=False).select_related("registered_by")[:DASHBOARD_RECENT_PATIENTS],
        "recent_activities": ActivityLog.objects.filter(user=request.user)[:DASHBOARD_RECENT_ACTIVITIES],
        "current_admissions": Admission.objects.filter(discharge_date__isnull=True)
                              .select_related("patient")[:DASHBOARD_CURRENT_ADMISSIONS],
        "my_registered": Patient.objects.filter(registered_by=request.user, is_archived=False).count(),
    })
