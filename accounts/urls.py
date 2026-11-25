"""URLs under /accounts/ (namespace "accounts")."""
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.HospitalLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),  # POST only (CSRF-protected)
    path("profile/", views.profile, name="profile"),
    path("password/", views.HospitalPasswordChangeView.as_view(), name="password_change"),
    path("administrators/", views.admin_list, name="admin_list"),
    path("administrators/new/", views.admin_create, name="admin_create"),
    path("administrators/<int:pk>/edit/", views.admin_update, name="admin_update"),
    path("administrators/<int:pk>/toggle/", views.admin_toggle, name="admin_toggle"),
    path("administrators/<int:pk>/password/", views.admin_reset_password, name="admin_reset_password"),
]
