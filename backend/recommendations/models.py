from django.db import models
import random
from backend.models import Attraction
class AttractionPopularity(models.Model):
    attraction = models.OneToOneField(Attraction, on_delete=models.CASCADE, primary_key=True, related_name='popularity')
    view_count = models.IntegerField(default=random.randint(0, 100))

    def __str__(self):
        return f"{self.attraction.name}: {self.view_count} views"