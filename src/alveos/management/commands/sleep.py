from django.core.management.base import BaseCommand, CommandError
from time import sleep

class Command(BaseCommand):
    help = 'Sleep (for testing)'

    def handle(self, *args, **options):
        sleep(10)

