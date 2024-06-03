from django.urls import path
from .views import DestinationRecommendationView


urlpatterns = [
   path('destinations/', DestinationRecommendationView.as_view(), name='destination_recommendation'),
]