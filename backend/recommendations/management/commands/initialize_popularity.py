# backend/recommendations/management/commands/initialize_popularity.py
from django.core.management.base import BaseCommand
from backend.models import Attraction
from backend.recommendations.models import AttractionPopularity
import random

class Command(BaseCommand):
    help = 'Initialize popularity data for all attractions'

    def handle(self, *args, **kwargs):
        attractions = Attraction.objects.all()
        for attraction in attractions:
            try:
                popularity, created = AttractionPopularity.objects.get_or_create(
                    attraction=attraction,
                    defaults={'view_count': random.randint(0, 100)}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created popularity for attraction: {attraction.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Popularity already exists for attraction: {attraction.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating popularity for attraction: {attraction.name}. Error: {str(e)}'))
