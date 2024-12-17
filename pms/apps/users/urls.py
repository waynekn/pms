from django.urls import path, include
from .views import (HomeView, ProfilePageView,
                    CSRFtokenView, FrontendView, GoogleLogin,)


urlpatterns = [
    path('', FrontendView.as_view(), name='frontend'),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/google/',
         GoogleLogin.as_view(), name='google_login'),
    path('user/<str:username>/', ProfilePageView.as_view(), name='profile_page'),
    path('csrftoken/', CSRFtokenView.as_view(), name='get_csrftoken'),
]
