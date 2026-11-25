"""Reports page, activity logs (Super Admin) and CSV export."""
import csv

from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.models import CustomUser
from core.constants import ACTIVITY_LOG_PER_PAGE, REPORT_CHART_MONTHS, TOP_ACTIVITY_TYPES
from core.decorators import staff_required, super_admin_required
from core.models import ActivityLog
from core.utils import log_activity, paginate, querystring
from patients.models import Patient

from . import services


@staff_required
def overview(request):
    """Reports page: charts for everyone, extra system-wide tables for the Super Admin."""
    context = {
        "stats": services.headline_stats(),
        "charts": {
            "monthly": services.registrations_by_month(REPORT_CHART_MONTHS),
            "gender": services.gender_breakdown(),
            "status": services.status_breakdown(),
            "blood": services.blood_type_breakdown(),
            "ages": services.age_group_breakdown(),
        },
    }
    if request.user.is_super_admin:
        context["by_admin"] = (
            CustomUser.objects.filter(role=CustomUser.Role.ADMIN)
            .annotate(registered=Count("registered_patients", filter=Q(registered_patients__is_archived=False)))
            .order_by("-registered", "username"))
        context["activity_by_action"] = (
            ActivityLog.objects.values("action").annotate(c=Count("id")).order_by("-c")[:TOP_ACTIVITY_TYPES])
    return render(request, "reports/overview.html", context)


@super_admin_required
def activity_logs(request):
    """Audit log viewer with filters (Super Admin only)."""
    q = request.GET.get("q", "").strip()
    action = request.GET.get("action", "")
    user_id = request.GET.get("user", "")
    logs = ActivityLog.objects.select_related("user")
    if q:
        logs = logs.filter(Q(description__icontains=q) | Q(user__username__icontains=q))
    if action in ActivityLog.Action.values:
        logs = logs.filter(action=action)
    if user_id.isdigit():
        logs = logs.filter(user_id=int(user_id))
    page_obj, page_range = paginate(request, logs, ACTIVITY_LOG_PER_PAGE)
    return render(request, "reports/activity_logs.html", {
        "page_obj": page_obj, "page_range": page_range, "base_qs": querystring(request),
        "q": q, "action": action, "user_id": user_id,
        "actions": ActivityLog.Action.choices,
        "users": CustomUser.objects.order_by("username"),
    })


@super_admin_required
def export_patients_csv(request):
    """Download every patient as a CSV file (Super Admin only)."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="patients_{timezone.localdate()}.csv"'
    writer = csv.writer(response)
    writer.writerow(["Patient ID", "Last name", "First name", "Middle name", "Date of birth", "Age", "Gender",
                     "Civil status", "Contact", "Email", "City", "Province", "Status", "Registered at",
                     "Registered by", "Archived"])
    for p in Patient.objects.select_related("registered_by").order_by("patient_id"):
        writer.writerow([p.patient_id, p.last_name, p.first_name, p.middle_name, p.date_of_birth, p.age,
                         p.get_gender_display(), p.get_civil_status_display(), p.contact_number, p.email,
                         p.city, p.province, p.get_status_display(),
                         timezone.localtime(p.registered_at).strftime("%Y-%m-%d %H:%M"),
                         p.registered_by.username if p.registered_by else "", "yes" if p.is_archived else "no"])
    log_activity(request.user, ActivityLog.Action.EXPORT, "Exported patient list to CSV", request)
    return response
