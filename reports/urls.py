"""URLs under /reports/ (namespace "reports")."""
from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("activity-logs/", views.activity_logs, name="activity_logs"),
    path("export/patients.csv", views.export_patients_csv, name="export_patients"),
]
