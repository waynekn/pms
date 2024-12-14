from typing import Any
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'users/home.html'


def csrf_token_view(request: HttpRequest):
    """
    Retrieve a CSRF token and return it to the client.

    This view generates a CSRF token and returns it in a JSON response. It is only 
    used during development when the client's origin is different from the API's origin.
    This enables the client to make POST without getting the Forbidden (403) response.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing the CSRF token.
    """
    return JsonResponse({'csrftoken': get_token(request)})


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


# class LoginAPI():
#     refresh = str(RefreshToken.for_user(user_instance))
#     access = str(RefreshToken.for_user(user_instance).access_token)
