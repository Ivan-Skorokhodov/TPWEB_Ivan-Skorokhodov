from django.core.management.base import BaseCommand
from app.context_processors import cache_popular_tags


class Command(BaseCommand):

    def handle(self, *args, **options):
        cache_popular_tags()
