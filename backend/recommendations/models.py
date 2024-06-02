from django.db import models
import random
from django.contrib.auth.models import User
from backend.models import Attraction
class AttractionPopularity(models.Model):
    attraction = models.OneToOneField(Attraction, on_delete=models.CASCADE, primary_key=True, related_name='popularity')
    view_count = models.IntegerField(default=random.randint(0, 100))

    def __str__(self):
        return f"{self.attraction.name}: {self.view_count} views"
    

class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    search_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched for {self.attraction.name} at {self.search_time}"

