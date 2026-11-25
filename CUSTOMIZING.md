# How to change things quickly

Rule of thumb: **look = `templates/` + `static/`**, **behaviour = `views.py`**, **data = `models.py`**,
**checks on typed data = `forms.py`**, **numbers = `core/constants.py`**. Every file starts with a comment saying what it does.

## 1. "I want to change ..." cheat sheet

| I want to change | Edit this |
|---|---|
| Hospital name, tagline, address, Patient ID prefix, rows per page | In the app: **System settings** (Super Admin). No code. |
| Colours of the whole system | `static/css/main.css` -> `--hms-blue`, `--hms-teal` at the top |
| Sidebar menu items | `templates/partials/_sidebar.html` |
| Top bar (search, bell, user menu) | `templates/partials/_topbar.html` |
| Login page | `templates/accounts/login.html` |
| Super Admin dashboard cards / charts | `templates/dashboard/super_admin.html` (what it shows) and `dashboard/views.py` (data it receives) |
| Admin dashboard | `templates/dashboard/admin.html` and `dashboard/views.py` |
| How many rows/months/days dashboards and charts show | `core/constants.py` |
| Max photo size, earliest birth year, age groups | `core/constants.py` |
| Patient registration form layout | `templates/patients/form.html` |
| Patient form rules (required, duplicates, birth date) | `patients/forms.py` |
| Patient table columns / buttons | `templates/patients/list.html` |
| Patient search, sorting, filters | `patients/views.py` -> `_apply_search`, `_apply_sort` |
| Patient profile page | `templates/patients/detail.html` |
| Printed patient sheet | `templates/patients/print.html` |
| Patient ID format (PAT-2026-00001) | `patients/models.py` -> `generate_patient_id` |
| Statistics numbers and charts data | `reports/services.py` |
| Who can open which page | The decorator above each view (`@super_admin_required`, `@staff_required`, `@admin_required`) in `views.py`; decorators are in `core/decorators.py` |
| Extra Admin permissions (like "can archive") | `accounts/models.py` (flags) + `core/decorators.py` + `accounts/forms.py` |
| Which actions are recorded in the audit log | call `log_activity(...)` in the view; action types are in `core/models.py` -> `ActivityLog.Action` |
| Database connection | `.env` (host, port, user, password, database) |
| Security / session timeout / time zone | `hms/settings.py` |
| Demo data | `core/management/commands/seed_data.py` |

## 2. Add a new field to patients (example: "Occupation")

1. `patients/models.py` -> in `Patient` add `occupation = models.CharField(max_length=80, blank=True)`
2. `patients/forms.py` -> add `"occupation"` to `PatientForm.Meta.fields`
3. `templates/patients/form.html` -> add `{% include "partials/_field.html" with field=pf.occupation col="col-md-4" %}`
4. Show it: `templates/patients/detail.html` and `templates/patients/print.html`
5. Update the database (run in the project folder):
   ```bash
   python manage.py makemigrations patients
   python manage.py migrate
   ```
   Refresh SCHEMAS in MySQL Workbench and the new column is there.

The same 5 steps work for emergency contact (`EmergencyContact`, `EmergencyContactForm`, `ef.`) and medical info
(`MedicalInformation`, `MedicalInformationForm`, `mf.`).

## 3. Add a new page (example: "Appointments list")

1. `appointments/views.py` -> a function with a role decorator and `return render(request, "appointments/list.html", {...})`
2. `appointments/urls.py` -> `path("", views.appointment_list, name="list")` and set `app_name = "appointments"`
3. `hms/urls.py` -> `path("appointments/", include("appointments.urls"))`
4. `hms/settings.py` -> add `"appointments"` to `INSTALLED_APPS` (only needed for a new app with models)
5. `templates/appointments/list.html` -> start with `{% extends "base.html" %}` and fill `{% block content %}`
6. `templates/partials/_sidebar.html` -> add a link: `{% url 'appointments:list' %}`

## 4. Reusable pieces (use these instead of copy-pasting HTML)

- **Form field:** `{% include "partials/_field.html" with field=form.name col="col-md-6" %}`
- **Stat card:** `{% include "partials/_stat_card.html" with label="..." value=... icon="people-fill" color="blue" url="/patients/" %}`
- **Pagination:** `{% include "partials/_pagination.html" %}` after `page_obj, page_range = paginate(request, queryset, 10)`
- **Confirm pop-up:** add `data-confirm="Are you sure?" data-confirm-title="Title" data-confirm-btn="Yes"` to any `<form method="post">`
- **Save to audit log:** `log_activity(request.user, ActivityLog.Action.UPDATE, "what happened", request)`
- **Icons:** any name from https://icons.getbootstrap.com, used as `<i class="bi bi-NAME"></i>`

## 5. Project map

```
.env                     database + secret settings (edit this first)
hms/                     project config: settings.py, urls.py
core/                    shared: constants.py, decorators.py, utils.py, models (audit log, settings), seed_data command
accounts/                login, roles, Admin account management
dashboard/               the two dashboards
patients/                registration + patient records
admissions/              admit / discharge
reports/                 services.py (statistics), reports page, activity logs, CSV export
templates/               HTML (one folder per app + partials/ for reusable pieces)
static/css/main.css      all styling      static/js/main.js    all JavaScript
database/                MySQL scripts, backups, ready-made .sql files
```

## 6. Habit that saves time
After any change run `python manage.py check` (finds mistakes in seconds) and, before sharing,
`python manage.py test` (21 tests confirm nothing broke).
