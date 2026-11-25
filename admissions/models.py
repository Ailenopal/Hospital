"""Admission record: one row per hospital stay. discharge_date empty = patient is still admitted."""
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

from patients.models import Patient


class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="admissions")
    admission_date = models.DateTimeField(default=timezone.now)
    ward = models.CharField(max_length=80)
    room_number = models.CharField(max_length=20, blank=True)
    attending_physician = models.CharField(max_length=120)
    reason = models.TextField("Reason for admission / diagnosis")
    admitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="admissions_made")

    discharge_date = models.DateTimeField(null=True, blank=True)
    discharge_notes = models.TextField(blank=True)
    discharged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="discharges_made")

    class Meta:
        ordering = ["-admission_date"]
        constraints = [
            # A patient can only have ONE open admission at a time.
            models.UniqueConstraint(
                fields=["patient"], condition=Q(discharge_date__isnull=True),
                name="one_active_admission_per_patient"),
        ]

    def __str__(self):
        return f"{self.patient.patient_id} admitted {self.admission_date:%Y-%m-%d}"

    @property
    def is_active(self):
        return self.discharge_date is None

    @property
    def length_of_stay(self):
        end = self.discharge_date or timezone.now()
        days = (end - self.admission_date).days
        return f"{days} day{'s' if days != 1 else ''}"
