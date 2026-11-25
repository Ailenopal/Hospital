"""Pages for sign-in, own profile/password, and Administrator management (Super Admin only)."""
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from core.decorators import super_admin_required
from core.constants import ADMIN_LIST_PER_PAGE
from core.models import ActivityLog
from core.utils import log_activity, paginate, querystring

from .forms import (AdminCreateForm, AdminUpdateForm, ChangePasswordForm,
                    LoginForm, ProfileForm, ResetPasswordForm)
from .models import CustomUser


class HospitalLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class HospitalPasswordChangeView(auth_views.PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = ChangePasswordForm
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        messages.success(self.request, "Your password was changed.")
        log_activity(self.request.user, ActivityLog.Action.ACCOUNT, "Changed own password", self.request)
        return super().form_valid(form)


@login_required
def profile(request):
    """My profile: any signed-in user edits their own name, email and phone."""
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_activity(request.user, ActivityLog.Action.UPDATE, "Updated own profile", request)
        messages.success(request, "Profile updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})


# ---------------- Administrator management (Super Admin only) ----------------

@super_admin_required
def admin_list(request):
    """Administrators page: search and filter all accounts. Super Admin only."""
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    users = CustomUser.objects.all().order_by("-role", "username")
    if q:
        users = users.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q)
            | Q(last_name__icontains=q) | Q(email__icontains=q)
        )
    if status == "active":
        users = users.filter(is_active=True)
    elif status == "inactive":
        users = users.filter(is_active=False)
    page_obj, page_range = paginate(request, users, ADMIN_LIST_PER_PAGE)
    return render(request, "accounts/admin_list.html", {
        "page_obj": page_obj, "page_range": page_range, "base_qs": querystring(request),
        "q": q, "status": status,
    })


@super_admin_required
def admin_create(request):
    """Create a new Admin account. The role is always "admin"."""
    form = AdminCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.created_by = request.user
        user.save()
        log_activity(request.user, ActivityLog.Action.ACCOUNT, f"Created Admin account '{user.username}'", request)
        messages.success(request, f"Admin account '{user.username}' was created.")
        return redirect("accounts:admin_list")
    return render(request, "accounts/admin_form.html", {"form": form, "is_create": True})


@super_admin_required
def admin_update(request, pk):
    """Edit an Admin: details, permissions, active/inactive."""
    target = get_object_or_404(CustomUser, pk=pk, role=CustomUser.Role.ADMIN)
    form = AdminUpdateForm(request.POST or None, instance=target)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_activity(request.user, ActivityLog.Action.ACCOUNT, f"Updated Admin account '{target.username}'", request)
        messages.success(request, f"Account '{target.username}' was updated.")
        return redirect("accounts:admin_list")
    return render(request, "accounts/admin_form.html", {"form": form, "target": target, "is_create": False})


@super_admin_required
@require_POST
def admin_toggle(request, pk):
    """Deactivate / reactivate an Admin (POST only). A deactivated Admin cannot sign in."""
    target = get_object_or_404(CustomUser, pk=pk, role=CustomUser.Role.ADMIN)
    target.is_active = not target.is_active
    target.save(update_fields=["is_active"])
    state = "activated" if target.is_active else "deactivated"
    log_activity(request.user, ActivityLog.Action.ACCOUNT, f"{state.title()} Admin account '{target.username}'", request)
    messages.success(request, f"Account '{target.username}' was {state}.")
    return redirect("accounts:admin_list")


@super_admin_required
def admin_reset_password(request, pk):
    """Super Admin sets a new password for an Admin."""
    target = get_object_or_404(CustomUser, pk=pk, role=CustomUser.Role.ADMIN)
    form = ResetPasswordForm(target, request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_activity(request.user, ActivityLog.Action.ACCOUNT, f"Reset password for '{target.username}'", request)
        messages.success(request, f"Password for '{target.username}' was reset.")
        return redirect("accounts:admin_list")
    return render(request, "accounts/admin_password.html", {"form": form, "target": target})
