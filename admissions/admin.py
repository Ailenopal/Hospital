"""Django built-in admin registration for admissions."""
from django.contrib import admin

from .models import Admission

admin.site.register(Admission)
