"""URLs for "/" and /dashboard/... (namespace "dashboard")."""
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/super-admin/", views.super_admin_dashboard, name="super_admin"),
    path("dashboard/admin/", views.admin_dashboard, name="admin"),
]
