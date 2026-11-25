"""URLs under /patients/ (namespace "patients")."""
from django.urls import path

from . import views

app_name = "patients"

urlpatterns = [
    path("", views.patient_list, name="list"),
    path("register/", views.patient_create, name="create"),
    path("<int:pk>/", views.patient_detail, name="detail"),
    path("<int:pk>/edit/", views.patient_update, name="update"),
    path("<int:pk>/archive/", views.patient_archive, name="archive"),
    path("<int:pk>/restore/", views.patient_restore, name="restore"),
    path("<int:pk>/print/", views.patient_print, name="print"),
]
