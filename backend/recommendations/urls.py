from django.urls import path
from .views import DestinationRecommendationView,DiaryRecommendationView


urlpatterns = [
   path('destinations/', DestinationRecommendationView.as_view(), name='destination_recommendation'),
   path('diaries',DiaryRecommendationView.as_view(),name='diary-recommendations')
]