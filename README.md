# Hospital Management System (Django)

Django 5 + Bootstrap 5. Role flow:

```
SUPER ADMIN (full system access)
   -> creates and manages Admin accounts
ADMIN (patient management access)
   -> Patient registration: register, edit, view, search, manage
HOSPITAL DATABASE (SQLite in development, PostgreSQL supported)
```

## Quick start (MySQL Workbench is the database)

1. **Create the database in MySQL Workbench.** Connect as `root`, open `database/setup_mysql.sql`
   (File > Open SQL Script) and run it. It creates `hms_db` and the user `hms_user`.
   *Or* import `database/hms_database_with_sample_data.sql` (Server > Data Import) to get tables and demo data at once.
2. **Check `.env`** in the project folder. It holds the connection (host, port, user, password, database).
   Make it match your Workbench connection.
3. **Run:**
   ```bash
   python -m venv venv
   venv\Scripts\activate            # macOS/Linux: source venv/bin/activate
   pip install -r requirements.txt
   python manage.py check_db         # confirms Django can reach MySQL
   python manage.py migrate          # creates the tables (skip if you imported the .sql file)
   python manage.py seed_data        # demo accounts and 25 sample patients (optional)
   python manage.py runserver
   ```
4. Open http://127.0.0.1:8000/ (needs internet for the Bootstrap, icon and Chart.js CDNs).
   Refresh SCHEMAS in Workbench and `hms_db` shows every record the system saves.

| Role        | Username     | Password      |
|-------------|--------------|---------------|
| Super Admin | `superadmin` | `Admin@12345` |
| Admin       | `admin1`     | `Admin@12345` |

Change these passwords outside local development. To create your own Super Admin instead of using
the seed: `python manage.py createsuperuser` (superusers automatically get the Super Admin role).

Run the tests: `python manage.py test` (21 tests: roles, validation, duplicates, admission cycle, audit log).


## MySQL Workbench connection

### Ready-made database files (no Django migrate needed)
`database/hms_database_with_sample_data.sql` is a full MySQL 8 export (16 tables, 25 patients, demo accounts) and
`database/hms_database_schema_only.sql` has empty tables. In Workbench: *Server > Data Import > Import from
Self-Contained File > Start Import*, refresh SCHEMAS, then set `DB_ENGINE=mysql` and run `python manage.py runserver`.

1. **Create the database.** In MySQL Workbench open your local connection (as `root`), choose *File > Open SQL Script*,
   pick `database/setup_mysql.sql` and run it. It creates `hms_db` and the user `hms_user` / `Hms@12345`.
2. **Point Django at MySQL.** In the terminal, run `database\set_mysql_env.bat` (Windows) or
   `source database/set_mysql_env.sh` (macOS/Linux).
3. **Create the tables and demo data:**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_data
   python manage.py runserver
   ```
4. **See the data in Workbench.** Click the refresh icon in the SCHEMAS panel, expand `hms_db > Tables`
   (`patients_patient`, `accounts_customuser`, `admissions_admission`, `core_activitylog` ...), and right-click a table >
   *Select Rows*.
5. **Make a Workbench connection for the app user (optional).** Home > the `+` next to *MySQL Connections*:
   Hostname `127.0.0.1`, Port `3306`, Username `hms_user`, password `Hms@12345`, Default Schema `hms_db`.

Notes: MySQL does not support conditional unique constraints, so Django skips two (a warning appears during `migrate`).
The same rules are still enforced by the application: duplicate patients are rejected by the form, and a patient already
admitted cannot be admitted again. Change the `hms_user` password in `setup_mysql.sql` and the env file for real use.

### PostgreSQL
`pip install psycopg2-binary`, then set `DB_ENGINE=postgres`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
(see `.env.example`) and run `migrate`. For production also set `DJANGO_DEBUG=False`, a real `DJANGO_SECRET_KEY`
and `DJANGO_ALLOWED_HOSTS`; HTTPS-only cookies and HSTS switch on automatically.

> **Want to change something?** Read `CUSTOMIZING.md`: a "change X -> edit file Y" table, how to add a field or a page,
> and the reusable template pieces. Tweakable numbers live in `core/constants.py`.

## Who can do what

| Feature | Super Admin | Admin |
|---|---|---|
| Own dashboard | Super Admin dashboard | Admin dashboard |
| Create / edit / deactivate Admin accounts, reset passwords, grant permissions | Yes | No (403) |
| Register, view, edit, search, print patients | Yes | Yes |
| Archive / restore patients | Yes | If granted |
| Admit / discharge | Yes | If granted |
| Reports and statistics | System-wide, CSV export | Patient statistics |
| Activity (audit) logs, System settings | Yes | No (403) |

An Admin can never create a Super Admin: the account form forces `role=admin`, and the form is unreachable to Admins.

## Project structure and purpose of each file

```
manage.py                     Django entry point
hms/settings.py               Settings (SQLite/PostgreSQL switch, custom user, sessions, security)
hms/urls.py                   Root URL routing, custom 403/404 handlers
accounts/                     Authentication and roles
  models.py                   CustomUser (role, phone, per-admin permission flags)
  forms.py                    Login, Admin create/update, password reset, profile forms
  views.py                    Login, profile, Administrator CRUD (Super Admin only)
  signals.py                  Writes login / logout / failed-login to the audit log
dashboard/                    views.py: role redirect, Super Admin and Admin dashboards
patients/                     Patient registration and records
  models.py                   Patient (auto ID, age, status, archive), EmergencyContact, MedicalInformation
  forms.py                    Validation: required fields, DOB, photo size, duplicate prevention
  views.py                    List (search/filter/sort/paginate), create, detail, edit, archive, restore, print
admissions/                   Admission model, admit and discharge views (updates patient status)
reports/                      services.py (DB statistics), overview charts, activity logs, CSV export
core/                         Shared code
  models.py                   ActivityLog (audit trail), SystemSetting (hospital name, ID prefix, page size)
  decorators.py               role_required, super_admin_required, staff_required, permission flags
  forms.py / utils.py         Bootstrap form mixin, log_activity(), pagination helpers
  context_processors.py       Hospital branding and notification feed for every page
  management/commands/seed_data.py   Demo data
  tests.py                    Automated tests
templates/                    base.html, error.html, partials/ (sidebar, topbar, field, pagination, modal ...),
                              and one folder per app
static/css/main.css           Blue and teal theme, responsive sidebar
static/js/main.js             Sidebar toggle, confirmation modal, photo preview, live age, alert auto-dismiss
media/                        Uploaded profile pictures (created at runtime)
```

## Key behaviours
- **Patient ID** is generated as `PAT-YYYY-00001` (prefix editable in System settings) with a retry on collisions.
- **Age** is calculated from the date of birth; the form also shows it live.
- **Duplicates**: a database constraint plus a case-insensitive form check on first name, last name and birth date (archived records excluded).
- **Status**: new patients are Active; admitting sets Admitted, discharging sets Discharged. A patient can have only one open admission, and admitted patients cannot be archived.
- **Archive** hides a record (soft delete) and it can be restored from the Archived view.
- **Security**: Django auth with PBKDF2 hashing, CSRF on every form, POST-only logout, 8-hour idle session timeout, password validators, role checks on every view, deactivated accounts cannot sign in, audit log with IP addresses.

## Backups and going live
- Back up the database any time with `database\backup_mysql.bat` (Windows) or `./database/backup_mysql.sh`
  (or in Workbench: Server > Data Export > `hms_db`). Restore with Server > Data Import.
- Before real use: change the `superadmin`/`admin1`/`admin2` passwords and the `hms_user` password (update `.env`),
  stop using `seed_data`, set `DJANGO_DEBUG=False`, a long random `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` in `.env`.
- MySQL is the only database used by this project.
