from django.urls import path
from .views import AttractionSearchView,search_diaries,FacilitySearch,NearbyFacilitySearch

urlpatterns = [
    path('attractions/', AttractionSearchView.as_view(), name='search-attractions'),
    path('diaries/', search_diaries, name='search_diaries'),
    path('facilitie_names/', FacilitySearch.as_view(), name='facility_search'),
    path('facilities/', NearbyFacilitySearch.as_view(), name='nearby_facility_search'),
]
