"""Admissions page, Admit patient, Discharge patient. Each also updates the patient status."""
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import permission_flag_required, staff_required
from core.models import ActivityLog, SystemSetting
from core.utils import log_activity, paginate, querystring
from patients.models import Patient

from .forms import AdmissionForm, DischargeForm, now_local
from .models import Admission


@staff_required
def admission_list(request):
    """Admissions page with tabs: currently admitted / discharged / all, plus search."""
    view = request.GET.get("view", "current")
    q = request.GET.get("q", "").strip()
    admissions = Admission.objects.select_related("patient", "admitted_by", "discharged_by")
    if view == "current":
        admissions = admissions.filter(discharge_date__isnull=True)
    elif view == "discharged":
        admissions = admissions.filter(discharge_date__isnull=False)
    else:
        view = "all"
    for term in q.split():
        admissions = admissions.filter(
            Q(patient__first_name__icontains=term) | Q(patient__last_name__icontains=term)
            | Q(patient__patient_id__icontains=term) | Q(ward__icontains=term)
            | Q(attending_physician__icontains=term))
    page_obj, page_range = paginate(request, admissions, SystemSetting.load().records_per_page)
    params = request.GET.copy()
    for key in ("page", "view"):
        params.pop(key, None)
    return render(request, "admissions/list.html", {
        "page_obj": page_obj, "page_range": page_range, "base_qs": querystring(request),
        "tab_qs": params.urlencode(), "view": view, "q": q,
        "counts": {
            "current": Admission.objects.filter(discharge_date__isnull=True).count(),
            "discharged": Admission.objects.filter(discharge_date__isnull=False).count(),
        },
    })


@staff_required
@permission_flag_required("may_manage_admissions")
def admission_create(request):
    """Admit a patient. Sets the patient status to Admitted. Needs the "manage admissions" permission."""
    initial = {"admission_date": now_local()}
    if request.GET.get("patient"):
        initial["patient"] = request.GET["patient"]
    form = AdmissionForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            admission = form.save(commit=False)
            admission.admitted_by = request.user
            admission.save()
            patient = admission.patient
            patient.status = Patient.Status.ADMITTED
            patient.save(update_fields=["status", "updated_at"])
        log_activity(request.user, ActivityLog.Action.ADMIT,
                     f"Admitted {patient.patient_id} to {admission.ward}", request)
        messages.success(request, f"{patient.full_name} was admitted to {admission.ward}.")
        return redirect("admissions:list")
    return render(request, "admissions/admit_form.html", {"form": form})


@staff_required
@permission_flag_required("may_manage_admissions")
def admission_discharge(request, pk):
    """Discharge a patient. Sets the patient status to Discharged. Needs the "manage admissions" permission."""
    admission = get_object_or_404(
        Admission.objects.select_related("patient"), pk=pk, discharge_date__isnull=True)
    form = DischargeForm(request.POST or None, instance=admission,
                         initial={"discharge_date": now_local()})
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            admission = form.save(commit=False)
            admission.discharged_by = request.user
            admission.save()
            patient = admission.patient
            patient.status = Patient.Status.DISCHARGED
            patient.save(update_fields=["status", "updated_at"])
        log_activity(request.user, ActivityLog.Action.DISCHARGE, f"Discharged {patient.patient_id}", request)
        messages.success(request, f"{patient.full_name} was discharged.")
        return redirect("admissions:list")
    return render(request, "admissions/discharge_form.html", {"form": form, "admission": admission})
