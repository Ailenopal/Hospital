"""Django built-in admin registration for patient tables."""
from django.contrib import admin

from .models import EmergencyContact, MedicalInformation, Patient

admin.site.register(Patient)
admin.site.register(EmergencyContact)
admin.site.register(MedicalInformation)
