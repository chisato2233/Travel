from django.urls import path
from .views import OptimalRouteView,MultiDestinationRouteView,RoutesImageView
from . import views
urlpatterns = [
    path('optimal/', OptimalRouteView.as_view(), name='optimal_route'),
    path('multi-destinations/',MultiDestinationRouteView.as_view(),name = 'multi_optimal_route'),
    path('global_map/',views.get_global_map, name='get_global_map'),
    path('routes_image/', RoutesImageView.as_view(), name='routes_image'),
]
