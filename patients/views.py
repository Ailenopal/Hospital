"""Patient pages: list (search/filter/sort), register, view, edit, archive, restore, print."""
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.decorators import permission_flag_required, staff_required
from core.models import ActivityLog, SystemSetting
from core.utils import log_activity, paginate, querystring

from .forms import EmergencyContactForm, MedicalInformationForm, PatientForm
from .models import EmergencyContact, MedicalInformation, Patient

SORT_FIELDS = {
    "patient_id": ("patient_id",),
    "name": ("last_name", "first_name"),
    "gender": ("gender",),
    "age": ("date_of_birth",),     # reversed below: older DOB = higher age
    "contact": ("contact_number",),
    "registered": ("registered_at",),
    "status": ("status",),
}
SORT_LABELS = [("patient_id", "Patient ID"), ("name", "Name"), ("gender", "Gender"), ("age", "Age"),
               ("contact", "Contact"), ("registered", "Registered"), ("status", "Status")]


# ---------------------------------------------------------------------------
# Patient list: search, filter, sort, paginate  (each step is its own helper)
# ---------------------------------------------------------------------------

def _apply_search(patients, text):
    """Every word typed must match the name, Patient ID or contact number ("juan cruz" works)."""
    for term in text.split():
        patients = patients.filter(
            Q(first_name__icontains=term) | Q(middle_name__icontains=term) | Q(last_name__icontains=term)
            | Q(patient_id__icontains=term) | Q(contact_number__icontains=term)
        )
    return patients


def _apply_sort(patients, sort, direction):
    """Order the list. Age is stored as a birth date, so its direction is flipped."""
    if sort == "age":
        direction = "asc" if direction == "desc" else "desc"
    prefix = "-" if direction == "desc" else ""
    return patients.order_by(*[prefix + field for field in SORT_FIELDS[sort]])


def _build_sort_headers(request, sort, direction):
    """Clickable column headers. Clicking the active column flips asc/desc."""
    headers = []
    for key, label in SORT_LABELS:
        params = request.GET.copy()
        params.pop("page", None)
        params["sort"] = key
        params["dir"] = "desc" if (key == sort and direction == "asc") else "asc"
        headers.append({"key": key, "label": label, "url": params.urlencode(),
                        "active": key == sort, "dir": direction})
    return headers


@staff_required
def patient_list(request):
    """All Patients page: GET parameters q (search), status, archived, sort, dir, page."""
    text = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    archived = request.GET.get("archived") == "1"
    sort = request.GET.get("sort", "registered")
    direction = request.GET.get("dir", "desc")
    if sort not in SORT_FIELDS:
        sort = "registered"

    patients = Patient.objects.filter(is_archived=archived)
    patients = _apply_search(patients, text)
    if status in Patient.Status.values:
        patients = patients.filter(status=status)
    patients = _apply_sort(patients, sort, direction)

    page_obj, page_range = paginate(request, patients, SystemSetting.load().records_per_page)
    return render(request, "patients/list.html", {
        "page_obj": page_obj, "page_range": page_range,
        "base_qs": querystring(request),
        "headers": _build_sort_headers(request, sort, direction),
        "q": text, "status": status, "archived": archived,
        "statuses": Patient.Status.choices,
        "total_count": page_obj.paginator.count,
    })


# ---------------------------------------------------------------------------
# Create / edit / view / archive / print
# ---------------------------------------------------------------------------

def _save_patient_forms(request, pf, ef, mf, creating):
    """Shared save logic for create and update."""
    with transaction.atomic():
        patient = pf.save(commit=False)
        if creating:
            patient.registered_by = request.user
        patient.save()
        contact = ef.save(commit=False)
        contact.patient = patient
        contact.save()
        medical = mf.save(commit=False)
        medical.patient = patient
        medical.save()
    return patient


@staff_required
def patient_create(request):
    """Register a new patient. Saves Patient + EmergencyContact + MedicalInformation together."""
    pf = PatientForm(request.POST or None, request.FILES or None)
    ef = EmergencyContactForm(request.POST or None, prefix="emergency")
    mf = MedicalInformationForm(request.POST or None, prefix="medical")
    if request.method == "POST":
        if all([pf.is_valid(), ef.is_valid(), mf.is_valid()]):
            patient = _save_patient_forms(request, pf, ef, mf, creating=True)
            log_activity(request.user, ActivityLog.Action.CREATE,
                         f"Registered patient {patient.patient_id} ({patient.full_name})", request)
            messages.success(request, f"Patient registered successfully. Patient ID: {patient.patient_id}")
            return redirect("patients:detail", pk=patient.pk)
        messages.error(request, "Please correct the highlighted fields and try again.")
    return render(request, "patients/form.html", {"pf": pf, "ef": ef, "mf": mf, "is_create": True})


@staff_required
def patient_detail(request, pk):
    """Patient profile page with all details and admission history."""
    patient = get_object_or_404(
        Patient.objects.select_related("registered_by"), pk=pk)
    return render(request, "patients/detail.html", {
        "patient": patient,
        "emergency": getattr(patient, "emergency_contact", None),
        "medical": getattr(patient, "medical_info", None),
        "admissions": patient.admissions.select_related("admitted_by", "discharged_by"),
        "current_admission": patient.current_admission,
    })


@staff_required
def patient_update(request, pk):
    """Edit an existing patient (same three forms as registration)."""
    patient = get_object_or_404(Patient, pk=pk)
    contact = getattr(patient, "emergency_contact", None) or EmergencyContact(patient=patient)
    medical = getattr(patient, "medical_info", None) or MedicalInformation(patient=patient)
    pf = PatientForm(request.POST or None, request.FILES or None, instance=patient)
    ef = EmergencyContactForm(request.POST or None, instance=contact, prefix="emergency")
    mf = MedicalInformationForm(request.POST or None, instance=medical, prefix="medical")
    if request.method == "POST":
        if all([pf.is_valid(), ef.is_valid(), mf.is_valid()]):
            _save_patient_forms(request, pf, ef, mf, creating=False)
            log_activity(request.user, ActivityLog.Action.UPDATE,
                         f"Updated patient {patient.patient_id} ({patient.full_name})", request)
            messages.success(request, "Patient record updated.")
            return redirect("patients:detail", pk=patient.pk)
        messages.error(request, "Please correct the highlighted fields and try again.")
    return render(request, "patients/form.html", {
        "pf": pf, "ef": ef, "mf": mf, "patient": patient, "is_create": False})


@staff_required
@permission_flag_required("may_archive_patients")
@require_POST
def patient_archive(request, pk):
    """Archive = hide the record (soft delete). POST only. Admitted patients cannot be archived."""
    patient = get_object_or_404(Patient, pk=pk, is_archived=False)
    if patient.status == Patient.Status.ADMITTED:
        messages.error(request, "This patient is currently admitted. Discharge them before archiving.")
        return redirect("patients:detail", pk=pk)
    patient.is_archived = True
    patient.save(update_fields=["is_archived", "updated_at"])
    log_activity(request.user, ActivityLog.Action.ARCHIVE, f"Archived patient {patient.patient_id}", request)
    messages.success(request, f"{patient.full_name} was archived.")
    return redirect("patients:list")


@staff_required
@permission_flag_required("may_archive_patients")
@require_POST
def patient_restore(request, pk):
    """Bring an archived record back to the active list. POST only."""
    patient = get_object_or_404(Patient, pk=pk, is_archived=True)
    clash = Patient.objects.filter(
        first_name__iexact=patient.first_name, last_name__iexact=patient.last_name,
        date_of_birth=patient.date_of_birth, is_archived=False).exists()
    if clash:
        messages.error(request, "Cannot restore: an active record with the same name and birth date exists.")
        return redirect("patients:detail", pk=pk)
    patient.is_archived = False
    patient.save(update_fields=["is_archived", "updated_at"])
    log_activity(request.user, ActivityLog.Action.RESTORE, f"Restored patient {patient.patient_id}", request)
    messages.success(request, f"{patient.full_name} was restored.")
    return redirect("patients:detail", pk=pk)


@staff_required
def patient_print(request, pk):
    """Printer-friendly registration sheet (no sidebar). Logged in the audit trail."""
    patient = get_object_or_404(Patient.objects.select_related("registered_by"), pk=pk)
    log_activity(request.user, ActivityLog.Action.PRINT, f"Printed record of {patient.patient_id}", request)
    return render(request, "patients/print.html", {
        "patient": patient,
        "emergency": getattr(patient, "emergency_contact", None),
        "medical": getattr(patient, "medical_info", None),
    })
