"""Admit and Discharge forms with date checks (no future dates, discharge after admission)."""
from datetime import timedelta

from django import forms
from django.utils import timezone

from core.constants import FUTURE_TOLERANCE_MINUTES
from core.forms import BootstrapFormMixin
from patients.models import Patient

from .models import Admission

DT_FORMAT = "%Y-%m-%dT%H:%M"


def _dt_widget():
    return forms.DateTimeInput(attrs={"type": "datetime-local"}, format=DT_FORMAT)


def now_local():
    return timezone.localtime(timezone.now()).replace(second=0, microsecond=0)


class AdmissionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Admission
        fields = ["patient", "admission_date", "ward", "room_number", "attending_physician", "reason"]
        widgets = {"admission_date": _dt_widget(), "reason": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["admission_date"].input_formats = [DT_FORMAT, "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        self.fields["patient"].queryset = (
            Patient.objects.filter(is_archived=False).exclude(status=Patient.Status.ADMITTED)
            .order_by("last_name", "first_name"))
        self.fields["patient"].label_from_instance = lambda p: f"{p.patient_id} - {p.last_name}, {p.first_name}"

    def clean_admission_date(self):
        value = self.cleaned_data["admission_date"]
        if value > timezone.now() + timedelta(minutes=FUTURE_TOLERANCE_MINUTES):
            raise forms.ValidationError("Admission date cannot be in the future.")
        return value


class DischargeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Admission
        fields = ["discharge_date", "discharge_notes"]
        widgets = {"discharge_date": _dt_widget(), "discharge_notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["discharge_date"].required = True
        self.fields["discharge_date"].input_formats = [DT_FORMAT, "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]

    def clean_discharge_date(self):
        value = self.cleaned_data["discharge_date"]
        if value < self.instance.admission_date:
            raise forms.ValidationError("Discharge cannot be earlier than the admission date.")
        if value > timezone.now() + timedelta(minutes=FUTURE_TOLERANCE_MINUTES):
            raise forms.ValidationError("Discharge date cannot be in the future.")
        return value
