from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path('avatar/update/',
         views.UserProfilePictureUpdateView.as_view(), name="update_avatar"),
    path('username/update/',
         views.UsernameUpdateView.as_view(), name="username_update"),
    path('accounts/delete/',
         views.UserAccountDeleteView.as_view(), name="account_delete"),
    path('accounts/register/', views.AccountRegsitrationView.as_view(),
         name='account_registration'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/google/',
         views.GoogleLogin.as_view(), name='google_login'),
    path('dj-rest-auth/token/refresh/',
         TokenRefreshView.as_view(), name="token_refresh"),
    path('accounts/', include('allauth.urls')),
]
