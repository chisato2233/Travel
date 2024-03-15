from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    # 其他URL模式...
]
