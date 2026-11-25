"""URLs under /settings/ (namespace "core")."""
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.system_settings, name="settings"),
]
