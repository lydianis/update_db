from django.core.management.base import BaseCommand
from update_app.utils.reset import reset_db

class Command(BaseCommand):
    help = 'Setzt die Datenbank auf den Anfangszustand zurück'

    def handle(self, *args, **options):
        reset_db()
        self.stdout.write(self.style.SUCCESS('Datenbank erfolgreich zurückgesetzt!'))