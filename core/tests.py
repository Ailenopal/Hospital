from datetime import date

from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from admissions.models import Admission
from patients.models import Patient

STRONG = "Str0ng!Pass#2026"


def patient_payload(**over):
    data = {
        "first_name": "Juan", "middle_name": "", "last_name": "Dela Cruz", "date_of_birth": "1990-05-14",
        "gender": "M", "civil_status": "single", "nationality": "Filipino", "contact_number": "09171234567",
        "email": "juan@example.com", "address": "1 Rizal St", "city": "Quezon City", "province": "Metro Manila",
        "zip_code": "1100",
        "emergency-name": "Maria Dela Cruz", "emergency-relationship": "Mother",
        "emergency-contact_number": "09179876543", "emergency-address": "",
        "medical-blood_type": "O+", "medical-allergies": "Penicillin", "medical-existing_conditions": "",
        "medical-medical_history": "", "medical-current_medications": "",
    }
    data.update(over)
    return data


class Base(TestCase):
    def setUp(self):
        self.sa = CustomUser.objects.create_superuser("boss", "b@x.com", "pass12345")
        self.admin = CustomUser.objects.create_user("nurse", "n@x.com", "pass12345", role="admin")


class RoleTests(Base):
    def test_superuser_gets_super_admin_role(self):
        self.assertTrue(self.sa.is_super_admin)

    def test_anonymous_redirected_to_login(self):
        r = self.client.get(reverse("patients:list"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/accounts/login/", r["Location"])

    def test_admin_blocked_from_super_admin_areas(self):
        self.client.force_login(self.admin)
        for name in ("accounts:admin_list", "accounts:admin_create", "core:settings",
                     "reports:activity_logs", "dashboard:super_admin"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 403, name)

    def test_super_admin_blocked_from_admin_dashboard_and_each_sees_own(self):
        self.client.force_login(self.sa)
        self.assertEqual(self.client.get(reverse("dashboard:admin")).status_code, 403)
        self.assertRedirects(self.client.get("/"), reverse("dashboard:super_admin"))
        self.client.force_login(self.admin)
        self.assertRedirects(self.client.get("/"), reverse("dashboard:admin"))

    def test_super_admin_creates_admin_role_is_forced(self):
        self.client.force_login(self.sa)
        r = self.client.post(reverse("accounts:admin_create"), {
            "username": "newadmin", "first_name": "N", "last_name": "A", "email": "na@x.com",
            "password1": STRONG, "password2": STRONG, "role": "super_admin", "is_superuser": "on"})
        self.assertEqual(r.status_code, 302)
        user = CustomUser.objects.get(username="newadmin")
        self.assertEqual(user.role, "admin")
        self.assertFalse(user.is_superuser)

    def test_deactivated_admin_cannot_login(self):
        self.client.force_login(self.sa)
        self.client.post(reverse("accounts:admin_toggle", args=[self.admin.pk]))
        self.admin.refresh_from_db()
        self.assertFalse(self.admin.is_active)
        self.client.logout()
        self.assertFalse(self.client.login(username="nurse", password="pass12345"))


class PatientTests(Base):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)

    def test_register_patient(self):
        r = self.client.post(reverse("patients:create"), patient_payload())
        p = Patient.objects.get()
        self.assertRedirects(r, reverse("patients:detail", args=[p.pk]))
        self.assertRegex(p.patient_id, r"^PAT-\d{4}-00001$")
        self.assertEqual(p.registered_by, self.admin)
        self.assertEqual(p.emergency_contact.name, "Maria Dela Cruz")
        self.assertEqual(p.medical_info.blood_type, "O+")
        self.assertEqual(p.status, "active")

    def test_ids_are_sequential_and_unique(self):
        self.client.post(reverse("patients:create"), patient_payload())
        self.client.post(reverse("patients:create"), patient_payload(first_name="Pedro"))
        ids = sorted(Patient.objects.values_list("patient_id", flat=True))
        self.assertTrue(ids[0].endswith("00001") and ids[1].endswith("00002"))

    def test_duplicate_rejected_case_insensitive(self):
        self.client.post(reverse("patients:create"), patient_payload())
        r = self.client.post(reverse("patients:create"), patient_payload(first_name="JUAN"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Patient.objects.count(), 1)

    def test_validation_future_dob_and_missing_fields(self):
        r = self.client.post(reverse("patients:create"), patient_payload(date_of_birth="2999-01-01", city=""))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Patient.objects.count(), 0)

    def test_age_calculation(self):
        self.client.post(reverse("patients:create"), patient_payload(date_of_birth="2000-01-01"))
        self.assertEqual(Patient.objects.get().age, date.today().year - 2000 - (1 if (date.today().month, date.today().day) < (1, 1) else 0))

    def test_search_filter_sort_paginate(self):
        for name in ("Alpha", "Bravo", "Charlie"):
            self.client.post(reverse("patients:create"), patient_payload(first_name=name))
        url = reverse("patients:list")
        names = lambda **q: [p.first_name for p in self.client.get(url, q).context["page_obj"]]
        self.assertEqual(names(q="bravo"), ["Bravo"])
        self.assertEqual(sorted(names(q="PAT-")), ["Alpha", "Bravo", "Charlie"])
        self.assertEqual(len(names(q="09171234567")), 3)
        self.assertEqual(names(q="charlie dela"), ["Charlie"])
        self.assertEqual(names(sort="name", dir="asc"), ["Alpha", "Bravo", "Charlie"])
        self.assertEqual(self.client.get(url, {"status": "admitted"}).context["total_count"], 0)
        self.assertEqual(self.client.get(url, {"sort": "age", "dir": "desc"}).status_code, 200)

    def test_update_and_archive_restore(self):
        self.client.post(reverse("patients:create"), patient_payload())
        p = Patient.objects.get()
        self.client.post(reverse("patients:update", args=[p.pk]), patient_payload(city="Manila"))
        p.refresh_from_db()
        self.assertEqual(p.city, "Manila")
        self.client.post(reverse("patients:archive", args=[p.pk]))
        p.refresh_from_db()
        self.assertTrue(p.is_archived)
        self.assertEqual(self.client.get(reverse("patients:list")).context["total_count"], 0)
        self.client.post(reverse("patients:restore", args=[p.pk]))
        p.refresh_from_db()
        self.assertFalse(p.is_archived)

    def test_archive_requires_permission_flag(self):
        self.client.post(reverse("patients:create"), patient_payload())
        p = Patient.objects.get()
        self.admin.can_archive_patients = False
        self.admin.save()
        self.assertEqual(self.client.post(reverse("patients:archive", args=[p.pk])).status_code, 403)

    def test_print_and_detail_pages(self):
        self.client.post(reverse("patients:create"), patient_payload())
        p = Patient.objects.get()
        for name in ("patients:detail", "patients:print", "patients:update"):
            self.assertEqual(self.client.get(reverse(name, args=[p.pk])).status_code, 200)


class AdmissionTests(Base):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)
        self.client.post(reverse("patients:create"), patient_payload())
        self.patient = Patient.objects.get()

    def admit(self):
        return self.client.post(reverse("admissions:admit"), {
            "patient": self.patient.pk, "admission_date": "2020-01-01T08:00", "ward": "ICU",
            "room_number": "12", "attending_physician": "Dr. Tan", "reason": "Observation"})

    def test_admit_and_discharge_cycle(self):
        self.assertEqual(self.admit().status_code, 302)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.status, "admitted")
        adm = Admission.objects.get()
        r = self.client.post(reverse("admissions:discharge", args=[adm.pk]),
                             {"discharge_date": "2020-01-05T10:00", "discharge_notes": "ok"})
        self.assertEqual(r.status_code, 302)
        self.patient.refresh_from_db()
        adm.refresh_from_db()
        self.assertEqual(self.patient.status, "discharged")
        self.assertEqual(adm.discharged_by, self.admin)

    def test_cannot_admit_twice_or_archive_while_admitted(self):
        self.admit()
        self.assertEqual(self.admit().status_code, 200)  # patient no longer selectable
        self.assertEqual(Admission.objects.count(), 1)
        self.client.post(reverse("patients:archive", args=[self.patient.pk]))
        self.patient.refresh_from_db()
        self.assertFalse(self.patient.is_archived)

    def test_discharge_before_admission_rejected(self):
        self.admit()
        adm = Admission.objects.get()
        self.client.post(reverse("admissions:discharge", args=[adm.pk]),
                         {"discharge_date": "2019-01-01T10:00", "discharge_notes": ""})
        adm.refresh_from_db()
        self.assertIsNone(adm.discharge_date)


class DashboardAndReportTests(Base):
    def test_stats_are_dynamic(self):
        self.client.force_login(self.admin)
        self.client.post(reverse("patients:create"), patient_payload())
        r = self.client.get(reverse("dashboard:admin"))
        self.assertEqual(r.context["stats"]["total"], 1)
        self.assertEqual(r.context["stats"]["admins"], 1)
        self.assertEqual(self.client.get(reverse("reports:overview")).status_code, 200)

    def test_super_admin_pages_render_and_export(self):
        self.client.force_login(self.sa)
        for name in ("dashboard:super_admin", "accounts:admin_list", "accounts:admin_create", "core:settings",
                     "reports:overview", "reports:activity_logs", "patients:list", "admissions:list",
                     "admissions:admit", "accounts:profile", "accounts:password_change"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)
        self.assertEqual(self.client.get(reverse("reports:export_patients")).status_code, 200)

    def test_audit_log_records_login_and_create(self):
        from core.models import ActivityLog
        self.client.post(reverse("accounts:login"), {"username": "nurse", "password": "wrong"})
        self.client.post(reverse("accounts:login"), {"username": "nurse", "password": "pass12345"})
        self.client.post(reverse("patients:create"), patient_payload())
        actions = set(ActivityLog.objects.values_list("action", flat=True))
        self.assertTrue({"LOGIN", "LOGIN_FAILED", "CREATE"} <= actions)
