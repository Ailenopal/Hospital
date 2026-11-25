"""The user table. One CustomUser model holds both roles (Super Admin / Admin) plus per-admin permission flags."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Single user table with a role field. Super Admin creates Admin accounts."""

    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)
    phone = models.CharField(max_length=20, blank=True)
    # Fine-grained permissions the Super Admin can grant or withdraw per Admin
    can_archive_patients = models.BooleanField("Can archive patient records", default=True)
    can_manage_admissions = models.BooleanField("Can admit / discharge patients", default=True)
    created_by = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="created_accounts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["username"]

    def save(self, *args, **kwargs):
        if self.is_superuser:  # e.g. `createsuperuser`
            self.role = self.Role.SUPER_ADMIN
        super().save(*args, **kwargs)

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN

    @property
    def is_hospital_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    @property
    def initials(self):
        name = self.display_name.split()
        return "".join(part[0] for part in name[:2]).upper()

    @property
    def may_archive_patients(self):
        return self.is_super_admin or self.can_archive_patients

    @property
    def may_manage_admissions(self):
        return self.is_super_admin or self.can_manage_admissions

    def __str__(self):
        return f"{self.display_name} ({self.get_role_display()})"
