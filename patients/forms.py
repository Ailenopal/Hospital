"""Registration/edit forms with validation: required fields, birth date, photo size, duplicate patients."""
from datetime import date

from django import forms

from core.constants import MAX_PHOTO_BYTES, MIN_BIRTH_YEAR
from core.forms import BootstrapFormMixin

from .models import EmergencyContact, MedicalInformation, Patient


class PatientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "first_name", "middle_name", "last_name", "date_of_birth", "gender",
            "civil_status", "nationality", "profile_picture", "contact_number",
            "email", "address", "city", "province", "zip_code",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "address": forms.Textarea(attrs={"rows": 2}),
            "profile_picture": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        if dob > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        if dob.year < MIN_BIRTH_YEAR:
            raise forms.ValidationError("Enter a valid date of birth.")
        return dob

    def clean_profile_picture(self):
        pic = self.cleaned_data.get("profile_picture")
        if pic and hasattr(pic, "size") and pic.size > MAX_PHOTO_BYTES:
            raise forms.ValidationError("Profile picture must be 2 MB or smaller.")
        return pic

    def clean(self):
        cleaned = super().clean()
        first, last, dob = (cleaned.get(k) for k in ("first_name", "last_name", "date_of_birth"))
        if first and last and dob:
            duplicates = Patient.objects.filter(
                first_name__iexact=first.strip(), last_name__iexact=last.strip(),
                date_of_birth=dob, is_archived=False,
            ).exclude(pk=self.instance.pk)
            if duplicates.exists():
                existing = duplicates.first()
                raise forms.ValidationError(
                    f"A patient with the same name and birth date already exists ({existing.patient_id})."
                )
        return cleaned


class EmergencyContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ["name", "relationship", "contact_number", "address"]
        widgets = {"address": forms.Textarea(attrs={"rows": 2})}


class MedicalInformationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MedicalInformation
        fields = ["blood_type", "allergies", "existing_conditions", "medical_history", "current_medications"]
        widgets = {f: forms.Textarea(attrs={"rows": 2}) for f in
                   ("allergies", "existing_conditions", "medical_history", "current_medications")}
