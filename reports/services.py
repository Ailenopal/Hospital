"""Statistics used by dashboards and the reports page. Every number comes from the database."""
import calendar
from datetime import date, timedelta

from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone

from accounts.models import CustomUser
from core.constants import AGE_GROUPS
from core.models import ActivityLog
from patients.models import MedicalInformation, Patient


def active_patients():
    """Base queryset used by every statistic: patients that are not archived."""
    return Patient.objects.filter(is_archived=False)


def headline_stats():
    """The big numbers on dashboards: totals, admitted, discharged, admins, today, etc."""
    counts = active_patients().aggregate(
        total=Count("id"),
        active=Count("id", filter=Q(status=Patient.Status.ACTIVE)),
        admitted=Count("id", filter=Q(status=Patient.Status.ADMITTED)),
        discharged=Count("id", filter=Q(status=Patient.Status.DISCHARGED)),
    )
    today = timezone.localdate()
    counts["today"] = active_patients().filter(registered_at__date=today).count()
    counts["archived"] = Patient.objects.filter(is_archived=True).count()
    counts["admins"] = CustomUser.objects.filter(role=CustomUser.Role.ADMIN, is_active=True).count()
    counts["admins_inactive"] = CustomUser.objects.filter(role=CustomUser.Role.ADMIN, is_active=False).count()
    counts["activities_today"] = ActivityLog.objects.filter(created_at__date=today).count()
    return counts


def registrations_by_day(days=7):
    """Registrations per day for the last N days (line chart)."""
    today = timezone.localdate()
    start = today - timedelta(days=days - 1)
    rows = (active_patients().filter(registered_at__date__gte=start)
            .annotate(d=TruncDate("registered_at")).values("d").annotate(c=Count("id")))
    lookup = {r["d"]: r["c"] for r in rows}
    labels, values = [], []
    for i in range(days):
        day = start + timedelta(days=i)
        labels.append(day.strftime("%b %d"))
        values.append(lookup.get(day, 0))
    return {"labels": labels, "values": values}


def registrations_by_month(months=6):
    """Registrations per month for the last N months (bar chart)."""
    today = timezone.localdate()
    y, m = today.year, today.month
    buckets = []
    for _ in range(months):
        buckets.append((y, m))
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    buckets.reverse()
    start = date(buckets[0][0], buckets[0][1], 1)
    rows = (active_patients().filter(registered_at__date__gte=start)
            .annotate(m=TruncMonth("registered_at")).values("m").annotate(c=Count("id")))
    lookup = {(r["m"].year, r["m"].month): r["c"] for r in rows}
    return {
        "labels": [f"{calendar.month_abbr[mm]} {yy}" for yy, mm in buckets],
        "values": [lookup.get(b, 0) for b in buckets],
    }


def gender_breakdown():
    """Patient counts by gender (doughnut chart)."""
    labels = dict(Patient.Gender.choices)
    rows = active_patients().values("gender").annotate(c=Count("id")).order_by("gender")
    return {"labels": [labels[r["gender"]] for r in rows], "values": [r["c"] for r in rows]}


def status_breakdown():
    """Patient counts by status: Active / Admitted / Discharged."""
    labels = dict(Patient.Status.choices)
    rows = {r["status"]: r["c"] for r in active_patients().values("status").annotate(c=Count("id"))}
    return {"labels": [labels[s] for s in labels], "values": [rows.get(s, 0) for s in labels]}


def blood_type_breakdown():
    """Patient counts by blood type."""
    rows = (MedicalInformation.objects.filter(patient__is_archived=False)
            .values("blood_type").annotate(c=Count("id")).order_by("-c"))
    labels = dict(MedicalInformation.BloodType.choices)
    return {"labels": [labels[r["blood_type"]] for r in rows], "values": [r["c"] for r in rows]}


def age_group_breakdown():
    """Patient counts per age group (groups are defined in core/constants.py)."""
    groups = AGE_GROUPS
    counts = {g[0]: 0 for g in groups}
    today = date.today()
    for dob in active_patients().values_list("date_of_birth", flat=True):
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        for label, low, high in groups:
            if low <= age <= high:
                counts[label] += 1
                break
    return {"labels": list(counts), "values": list(counts.values())}
