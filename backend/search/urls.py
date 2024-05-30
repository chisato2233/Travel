from django.urls import path
from .views import AttractionSearchView,search_diaries

urlpatterns = [
    path('attractions/', AttractionSearchView.as_view(), name='search-attractions'),
    path('diaries/', search_diaries, name='search_diaries'),
]
