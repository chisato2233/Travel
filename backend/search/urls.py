from django.urls import path
from .views import AttractionSearchView

urlpatterns = [
    path('attractions/', AttractionSearchView.as_view(), name='search-attractions'),
]
