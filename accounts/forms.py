"""Forms for sign-in, Admin account create/edit, password reset and profile. All get Bootstrap styling from BootstrapFormMixin."""
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       SetPasswordForm, UserCreationForm)

from core.forms import BootstrapFormMixin

from .models import CustomUser


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username", "autofocus": True})
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})


class AdminCreateForm(BootstrapFormMixin, UserCreationForm):
    """Used by the Super Admin. The role is forced to ADMIN - a Super Admin cannot
    be created from this form, and Admins cannot reach it at all."""

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "phone",
                  "can_archive_patients", "can_manage_admissions")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("first_name", "last_name", "email"):
            self.fields[name].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.ADMIN
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class AdminUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone",
                  "can_archive_patients", "can_manage_admissions", "is_active")
        labels = {"is_active": "Account is active"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("first_name", "last_name", "email"):
            self.fields[name].required = True


class ResetPasswordForm(BootstrapFormMixin, SetPasswordForm):
    pass


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone")


class ChangePasswordForm(BootstrapFormMixin, PasswordChangeForm):
    pass
