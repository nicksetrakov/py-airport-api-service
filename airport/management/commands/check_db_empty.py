from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Check if the database is empty and populate it with fake data if it is"

    def handle(self, *args, **kwargs):
        self.stdout.write("Checking if database is empty...")
        try:
            connection = connections["default"]
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
            )
            row = cursor.fetchone()
            if row[0] == 0:
                self.stdout.write("Database is empty, generating fake data...")
                call_command("generate_fake_data")
            else:
                self.stdout.write("Database is not empty, no action taken.")
        except OperationalError:
            self.stdout.write("Database is not available.")
