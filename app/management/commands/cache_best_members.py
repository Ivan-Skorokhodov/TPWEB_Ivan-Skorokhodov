from django.core.management.base import BaseCommand
from app.context_processors import cache_best_members


class Command(BaseCommand):

    def handle(self, *args, **options):
        cache_best_members()
