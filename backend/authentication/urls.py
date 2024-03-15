# backend/authentication/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, GetUserView, UpdateUserView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/', GetUserView.as_view(), name='get_user'),
    path('update/', UpdateUserView.as_view(), name='update_user'),
]
