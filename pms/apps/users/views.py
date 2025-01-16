import os
from typing import Any
from dotenv import load_dotenv
from django.http import HttpRequest
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .serializers import SocialLoginSerializer

load_dotenv()

# Create your views here.


class GoogleLogin(SocialLoginView):
    """
    Handle Google auth using Authorization Code Grant
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.getenv('GOOGLE_REDIRECT_URL')
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
