"""URLs under /admissions/ (namespace "admissions")."""
from django.urls import path

from . import views

app_name = "admissions"

urlpatterns = [
    path("", views.admission_list, name="list"),
    path("admit/", views.admission_create, name="admit"),
    path("<int:pk>/discharge/", views.admission_discharge, name="discharge"),
]
