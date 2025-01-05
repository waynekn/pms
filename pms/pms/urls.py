"""
URL configuration for pms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path

from .views import FrontendView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^accounts/google/login/callback/$',
            FrontendView.as_view(), name='intercept_google_auth_code'),
    path('', include('apps.users.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('', include('apps.projects.urls')),
    re_path(r'^.*$', FrontendView.as_view(), name='react_frontend'),
]
