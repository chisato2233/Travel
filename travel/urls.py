"""
URL configuration for travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('backend.authentication.urls')),
    path('api/routes/',include('backend.tourist_routes.urls')),
    path('api/diaries/',include('backend.diaries.urls')),
    path('api/search/',include('backend.search.urls')),
    path('api/recommendations/', include('backend.recommendations.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # 添加登录URL
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)