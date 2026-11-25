"""BootstrapFormMixin (styles every form field) and the System settings form."""
from django import forms

from .models import SystemSetting


class BootstrapFormMixin:
    """Adds Bootstrap 5 classes to every widget. Put it FIRST in the MRO."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css = "form-select"
            else:
                css = "form-control"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css}".strip()


class SystemSettingForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = ["hospital_name", "tagline", "address", "phone", "email",
                  "registration_prefix", "records_per_page"]

    def clean_registration_prefix(self):
        return self.cleaned_data["registration_prefix"].strip().upper()
