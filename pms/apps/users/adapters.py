from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class CustomLoginRedirectAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """
        After login, redirect to the user's profile page using the URL name 'profile_page'.
        """
        if request.user.is_authenticated:
            return reverse('profile_page', kwargs={'username': request.user.username})
        return super().get_login_redirect_url(request)
