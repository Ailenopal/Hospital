"""Patient, EmergencyContact and MedicalInformation tables, including automatic Patient ID and age."""
from datetime import date

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import IntegrityError, models, transaction
from django.db.models import Q
from django.utils import timezone

from core.models import SystemSetting

phone_validator = RegexValidator(r"^[0-9+\-\s()]{7,20}$", "Enter a valid phone number (digits, +, -, spaces).")


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    class CivilStatus(models.TextChoices):
        SINGLE = "single", "Single"
        MARRIED = "married", "Married"
        WIDOWED = "widowed", "Widowed"
        SEPARATED = "separated", "Separated"
        DIVORCED = "divorced", "Divorced"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ADMITTED = "admitted", "Admitted"
        DISCHARGED = "discharged", "Discharged"

    # Personal information
    patient_id = models.CharField(max_length=24, unique=True, editable=False)
    first_name = models.CharField(max_length=60)
    middle_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    civil_status = models.CharField(max_length=12, choices=CivilStatus.choices)
    nationality = models.CharField(max_length=60, default="Filipino")
    profile_picture = models.ImageField(upload_to="patients/%Y/%m/", blank=True, null=True)

    # Contact information
    contact_number = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField(blank=True)
    address = models.TextField("Complete address")
    city = models.CharField("City / Municipality", max_length=80)
    province = models.CharField(max_length=80)
    zip_code = models.CharField("ZIP code", max_length=10)

    # Registration information
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    is_archived = models.BooleanField(default=False, db_index=True)
    registered_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="registered_patients"
    )

    class Meta:
        ordering = ["-registered_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name", "date_of_birth"],
                condition=Q(is_archived=False),
                name="unique_active_patient_identity",
            )
        ]

    def __str__(self):
        return f"{self.patient_id} - {self.full_name}"

    # ---- derived values ----
    @property
    def full_name(self):
        return " ".join(p for p in (self.first_name, self.middle_name, self.last_name) if p)

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @property
    def status_class(self):
        return {"active": "success", "admitted": "warning", "discharged": "secondary"}[self.status]

    @property
    def current_admission(self):
        return self.admissions.filter(discharge_date__isnull=True).first()

    @property
    def initials(self):
        return f"{self.first_name[:1]}{self.last_name[:1]}".upper()

    # ---- unique Patient ID: PREFIX-YEAR-00001 ----
    @classmethod
    def generate_patient_id(cls):
        prefix = SystemSetting.load().registration_prefix
        base = f"{prefix}-{timezone.localdate().year}-"
        last = cls.objects.filter(patient_id__startswith=base).order_by("-patient_id").first()
        number = int(last.patient_id.rsplit("-", 1)[1]) + 1 if last else 1
        return f"{base}{number:05d}"

    def save(self, *args, **kwargs):
        if self.patient_id:
            return super().save(*args, **kwargs)
        for _ in range(5):  # retry if two registrations race for the same number
            self.patient_id = self.generate_patient_id()
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError as exc:
                if "patient_id" not in str(exc):
                    raise
                self.patient_id = ""
        raise IntegrityError("Could not generate a unique Patient ID.")


class EmergencyContact(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="emergency_contact")
    name = models.CharField("Emergency contact person", max_length=120)
    relationship = models.CharField("Relationship to patient", max_length=60)
    contact_number = models.CharField("Emergency contact number", max_length=20, validators=[phone_validator])
    address = models.TextField("Emergency contact address", blank=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class MedicalInformation(models.Model):
    class BloodType(models.TextChoices):
        A_POS = "A+", "A+"
        A_NEG = "A-", "A-"
        B_POS = "B+", "B+"
        B_NEG = "B-", "B-"
        AB_POS = "AB+", "AB+"
        AB_NEG = "AB-", "AB-"
        O_POS = "O+", "O+"
        O_NEG = "O-", "O-"
        UNKNOWN = "unknown", "Unknown"

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="medical_info")
    blood_type = models.CharField(max_length=8, choices=BloodType.choices, default=BloodType.UNKNOWN)
    allergies = models.TextField("Known allergies", blank=True)
    existing_conditions = models.TextField("Existing medical conditions", blank=True)
    medical_history = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Medical information"

    def __str__(self):
        return f"Medical info for {self.patient.patient_id}"
