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


class CSRFtokenView(APIView):
    """
    Retrieve a CSRF token and return it to the client.

    This view generates a CSRF token and returns it in a JSON response. It is only 
    used during development when the client's origin is different from the API's origin.
    This enables the client to make POST without getting the Forbidden (403) response.
    """
    permission_classes = []

    def get(self, request: Request) -> Response:
        csrftoken = get_token(request)
        return Response({'csrftoken': csrftoken}, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    """
    Handle Google auth using Authorization Code Grant
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.getenv('GOOGLE_REDIRECT_URL')
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
