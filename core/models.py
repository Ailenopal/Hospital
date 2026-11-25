"""Shared tables: ActivityLog (audit trail) and SystemSetting (hospital name, ID prefix, rows per page)."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class SystemSetting(models.Model):
    """Single-row table holding hospital-wide configuration (Super Admin only)."""

    hospital_name = models.CharField(max_length=120, default="City General Hospital")
    tagline = models.CharField(max_length=160, blank=True, default="Compassionate care, trusted records")
    address = models.CharField(max_length=255, blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    registration_prefix = models.CharField(
        "Patient ID prefix", max_length=6, default="PAT",
        validators=[RegexValidator(r"^[A-Z0-9]{2,6}$", "Use 2-6 capital letters or digits.")],
    )
    records_per_page = models.PositiveSmallIntegerField(
        default=10, validators=[MinValueValidator(5), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = "System setting"

    def __str__(self):
        return self.hospital_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ActivityLog(models.Model):
    """Audit trail of important actions."""

    class Action(models.TextChoices):
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"
        LOGIN_FAILED = "LOGIN_FAILED", "Failed login"
        CREATE = "CREATE", "Create"
        UPDATE = "UPDATE", "Update"
        ARCHIVE = "ARCHIVE", "Archive"
        RESTORE = "RESTORE", "Restore"
        ADMIT = "ADMIT", "Admission"
        DISCHARGE = "DISCHARGE", "Discharge"
        ACCOUNT = "ACCOUNT", "Account"
        SETTINGS = "SETTINGS", "Settings"
        EXPORT = "EXPORT", "Export"
        PRINT = "PRINT", "Print"

    STYLES = {
        "LOGIN": ("box-arrow-in-right", "success"),
        "LOGOUT": ("box-arrow-right", "secondary"),
        "LOGIN_FAILED": ("shield-exclamation", "danger"),
        "CREATE": ("plus-circle", "primary"),
        "UPDATE": ("pencil-square", "info"),
        "ARCHIVE": ("archive", "warning"),
        "RESTORE": ("arrow-counterclockwise", "success"),
        "ADMIT": ("hospital", "primary"),
        "DISCHARGE": ("door-open", "success"),
        "ACCOUNT": ("person-gear", "primary"),
        "SETTINGS": ("gear", "secondary"),
        "EXPORT": ("download", "info"),
        "PRINT": ("printer", "secondary"),
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="activities",
    )
    action = models.CharField(max_length=20, choices=Action.choices)
    description = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.action} {self.description}"

    @property
    def icon(self):
        return self.STYLES.get(self.action, ("activity", "secondary"))[0]

    @property
    def color(self):
        return self.STYLES.get(self.action, ("activity", "secondary"))[1]
