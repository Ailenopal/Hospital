"""Writes sign-in, sign-out and failed sign-in events to the audit log automatically."""
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from core.models import ActivityLog
from core.utils import log_activity


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    """Audit-log every successful sign-in."""
    log_activity(user, ActivityLog.Action.LOGIN, f"{user.username} signed in", request)


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    """Audit-log every sign-out."""
    if user is not None:
        log_activity(user, ActivityLog.Action.LOGOUT, f"{user.username} signed out", request)


@receiver(user_login_failed)
def on_login_failed(sender, credentials, request=None, **kwargs):
    """Audit-log failed sign-in attempts (username only, never the password)."""
    username = credentials.get("username", "")
    log_activity(None, ActivityLog.Action.LOGIN_FAILED, f"Failed sign-in attempt for '{username}'", request)
