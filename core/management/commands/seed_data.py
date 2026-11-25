"""Development seed: python manage.py seed_data [--reset]"""
import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import CustomUser
from admissions.models import Admission
from core.models import ActivityLog, SystemSetting
from patients.models import EmergencyContact, MedicalInformation, Patient

PASSWORD = "Admin@12345"

FIRST = ["Juan", "Maria", "Jose", "Ana", "Carlo", "Liza", "Miguel", "Rosa", "Paolo", "Grace", "Ramon", "Isabel",
         "Andres", "Teresa", "Luis", "Carmen", "Daniel", "Elena", "Rafael", "Sofia", "Gabriel", "Lourdes",
         "Mateo", "Angela", "Victor"]
LAST = ["Dela Cruz", "Santos", "Reyes", "Garcia", "Mendoza", "Torres", "Ramos", "Flores", "Aquino", "Bautista",
        "Villanueva", "Castillo", "Navarro", "Domingo", "Aguilar", "Pascual", "Soriano", "Fernandez", "Salazar",
        "Valdez", "Rivera", "Tolentino", "Manalo", "Cruz", "Lim"]
CITIES = [("Quezon City", "Metro Manila", "1100"), ("Manila", "Metro Manila", "1000"),
          ("Cebu City", "Cebu", "6000"), ("Davao City", "Davao del Sur", "8000"),
          ("Baguio", "Benguet", "2600"), ("Iloilo City", "Iloilo", "5000")]
WARDS = ["General Ward", "Pediatrics", "Surgical Ward", "ICU", "Maternity"]
DOCTORS = ["Dr. A. Lopez", "Dr. B. Ramirez", "Dr. C. Tan", "Dr. D. Gonzales"]
REASONS = ["Pneumonia", "Dengue fever", "Post-operative care", "Hypertensive crisis", "Appendicitis", "Observation"]
ALLERGIES = ["", "", "Penicillin", "Peanuts", "Shellfish", "Sulfa drugs"]
CONDITIONS = ["", "Hypertension", "Type 2 diabetes", "Asthma", "", "Hyperlipidemia"]


class Command(BaseCommand):
    help = "Create demo accounts, patients, admissions and activity logs."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing patients/admissions first")

    @transaction.atomic
    def handle(self, *args, **opts):
        random.seed(7)
        if opts["reset"]:
            Admission.objects.all().delete()
            Patient.objects.all().delete()
            ActivityLog.objects.all().delete()

        setting = SystemSetting.load()
        setting.hospital_name = "City General Hospital"
        setting.address = "123 Health Avenue, Quezon City"
        setting.phone = "(02) 8123-4567"
        setting.email = "info@citygeneral.example"
        setting.save()

        sa, _ = CustomUser.objects.get_or_create(username="superadmin", defaults=dict(
            first_name="Sam", last_name="Reyes", email="superadmin@hms.example",
            role=CustomUser.Role.SUPER_ADMIN, is_staff=True, is_superuser=True))
        sa.set_password(PASSWORD)
        sa.save()

        admins = []
        for username, first, last in [("admin1", "Nina", "Cortez"), ("admin2", "Marco", "Dizon")]:
            user, _ = CustomUser.objects.get_or_create(username=username, defaults=dict(
                first_name=first, last_name=last, email=f"{username}@hms.example",
                role=CustomUser.Role.ADMIN, created_by=sa))
            user.set_password(PASSWORD)
            user.save()
            admins.append(user)

        if Patient.objects.exists():
            self.stdout.write(self.style.WARNING("Patients already exist - skipping sample patients (use --reset)."))
        else:
            now = timezone.now()
            patients = []
            for i in range(25):
                city, province, zip_code = random.choice(CITIES)
                first, last = FIRST[i], LAST[i]
                patient = Patient(
                    first_name=first, last_name=last, middle_name=random.choice(["", "Santos", "Lopez", "M."]),
                    date_of_birth=date.today() - timedelta(days=random.randint(365, 365 * 85)),
                    gender=random.choice(["M", "F"]), civil_status=random.choice(Patient.CivilStatus.values),
                    nationality="Filipino", contact_number=f"09{random.randint(100000000, 999999999)}",
                    email=f"{first.lower()}.{last.lower().replace(' ', '')}@example.com",
                    address=f"{random.randint(1, 300)} Rizal Street", city=city, province=province,
                    zip_code=zip_code, registered_by=random.choice(admins))
                patient.save()
                EmergencyContact.objects.create(
                    patient=patient, name=f"{random.choice(FIRST)} {patient.last_name}",
                    relationship=random.choice(["Spouse", "Parent", "Sibling", "Child"]),
                    contact_number=f"09{random.randint(100000000, 999999999)}", address=patient.address)
                MedicalInformation.objects.create(
                    patient=patient, blood_type=random.choice(MedicalInformation.BloodType.values),
                    allergies=random.choice(ALLERGIES), existing_conditions=random.choice(CONDITIONS),
                    medical_history="No significant surgical history." if i % 3 else "Appendectomy (2015).",
                    current_medications=random.choice(["", "Metformin 500mg", "Amlodipine 5mg", ""]))
                # spread registration dates over the last ~150 days
                registered = now - timedelta(days=random.randint(0, 150), hours=random.randint(0, 12))
                Patient.objects.filter(pk=patient.pk).update(registered_at=registered)
                patients.append(patient)

            # admissions: 5 current, 6 discharged
            for patient in patients[:5]:
                Admission.objects.create(
                    patient=patient, admission_date=now - timedelta(days=random.randint(0, 6), hours=3),
                    ward=random.choice(WARDS), room_number=str(random.randint(100, 420)),
                    attending_physician=random.choice(DOCTORS), reason=random.choice(REASONS),
                    admitted_by=random.choice(admins))
                Patient.objects.filter(pk=patient.pk).update(status=Patient.Status.ADMITTED)
            for patient in patients[5:11]:
                start = now - timedelta(days=random.randint(10, 60))
                Admission.objects.create(
                    patient=patient, admission_date=start, ward=random.choice(WARDS),
                    room_number=str(random.randint(100, 420)), attending_physician=random.choice(DOCTORS),
                    reason=random.choice(REASONS), admitted_by=random.choice(admins),
                    discharge_date=start + timedelta(days=random.randint(2, 8)),
                    discharge_notes="Recovered well. Follow-up in two weeks.",
                    discharged_by=random.choice(admins))
                Patient.objects.filter(pk=patient.pk).update(status=Patient.Status.DISCHARGED)

            for patient in patients[:10]:
                ActivityLog.objects.create(user=patient.registered_by, action="CREATE",
                                           description=f"Registered patient {patient.patient_id} ({patient.full_name})")
            ActivityLog.objects.create(user=sa, action="ACCOUNT", description="Created Admin account 'admin1'")
            ActivityLog.objects.create(user=sa, action="ACCOUNT", description="Created Admin account 'admin2'")

        self.stdout.write(self.style.SUCCESS("Seed complete."))
        self.stdout.write(f"  Super Admin : superadmin / {PASSWORD}")
        self.stdout.write(f"  Admin       : admin1 / {PASSWORD}   (also admin2)")
