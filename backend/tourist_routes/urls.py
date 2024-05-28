from django.urls import path
from .views import OptimalRouteView,MultiDestinationRouteView

urlpatterns = [
    path('optimal/', OptimalRouteView.as_view(), name='optimal_route'),
    path('multi-destinations/',MultiDestinationRouteView.as_view(),name = 'multi_optimal_route')
]
