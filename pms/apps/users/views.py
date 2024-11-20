from typing import Any
from django.http import HttpRequest
from django.shortcuts import redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'users/home.html'


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
