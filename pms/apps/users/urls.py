from django.urls import path, include
from .views import (HomeView, ProfilePageView, csrf_token_view)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('user/<str:username>/', ProfilePageView.as_view(), name='profile_page'),
    path('csrftoken/', csrf_token_view, name='get_csrftoken'),
]
