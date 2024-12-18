from django.urls import path, include
from .views import (ProfilePageView,
                    CSRFtokenView, GoogleLogin,)


urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/google/',
         GoogleLogin.as_view(), name='google_login'),
    path('user/<str:username>/', ProfilePageView.as_view(), name='profile_page'),
    path('csrftoken/', CSRFtokenView.as_view(), name='get_csrftoken'),
    path('accounts/', include('allauth.urls')),
]
