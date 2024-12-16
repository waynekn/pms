from typing import Any
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

# Create your views here.


class FrontendView(TemplateView):
    """
    Renders the `index.html` template for the frontend application.

    This view serves the `index.html` file, which references static assets
    built by Vite during the build process. The template includes the necessary
    CSS and JavaScript files to initialize the React-based frontend.
    """
    template_name = 'index.html'


class HomeView(TemplateView):
    template_name = 'users/home.html'


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


class ProfilePageView(LoginRequiredMixin, TemplateView):
    """
    Returns a user's profile page. If the user is not authenticated or is trying to view a profile
    that is not theirs, they will be redirected to the login page or the their own page.
    """
    template_name = 'users/profile_page.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | HttpResponseRedirect:
        username = kwargs.get('username')

        if request.user.username != username:
            # Redirect to the user's own profile if they are trying to access someone else's profile
            return redirect('profile_page', username=request.user.username)

        return super().dispatch(request, *args, **kwargs)
