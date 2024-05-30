# initialize_view_counts.py
import random
from backend.models import Attraction

def initialize_view_counts():
    attractions = Attraction.objects.all()
    for attraction in attractions:
        if attraction.view_count is None:
            attraction.view_count = random.randint(0, 100)
            attraction.save()

if __name__ == "__main__":
    initialize_view_counts()
