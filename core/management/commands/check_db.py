"""python manage.py check_db  - verifies the MySQL (Workbench) connection and lists the data."""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Test the database connection and show what is stored."

    def handle(self, *args, **options):
        cfg = connection.settings_dict
        self.stdout.write(f"Engine : {cfg['ENGINE']}\nServer : {cfg.get('HOST')}:{cfg.get('PORT')}  Database: {cfg['NAME']}  User: {cfg.get('USER')}")
        try:
            with connection.cursor() as cur:
                cur.execute("SELECT 1")
            tables = connection.introspection.table_names()
        except Exception as exc:  # noqa: BLE001
            self.stdout.write(self.style.ERROR(f"\nCONNECTION FAILED: {exc}"))
            self.stdout.write("Check: 1) MySQL server is running  2) the values in .env match your Workbench connection  "
                              "3) you ran database/setup_mysql.sql (creates hms_db and hms_user).")
            return
        self.stdout.write(self.style.SUCCESS(f"\nConnected. {len(tables)} tables found."))
        if not tables:
            self.stdout.write("Database is empty -> run: python manage.py migrate")
            return
        from patients.models import Patient
        from accounts.models import CustomUser
        self.stdout.write(f"Patients: {Patient.objects.count()}   Users: {CustomUser.objects.count()}")
