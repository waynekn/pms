from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from requests.exceptions import HTTPError
from django.utils.translation import gettext_lazy as _
from django.urls.exceptions import NoReverseMatch
from django.http import HttpRequest, HttpResponseBadRequest
from django.db import IntegrityError
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from .utils import slugify_username


class UserRetrievalSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a user's username.
    """

    class Meta:
        model = User
        fields = ['username']


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer class for `REST_AUTH`. 

    The fields defined here are what will be returned when
    `dj-rest-auth` retreives a `User` from the database.
    """
    class Meta:
        model = User
        fields = (
            "pk", "email", "username", "username_slug",
        )


try:
    from allauth.account import app_settings as allauth_account_settings
    from allauth.socialaccount.helpers import complete_social_login
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


class SocialLoginSerializer(serializers.Serializer):
    """
    Custom serializer for social login handling.

    Removes 'scope' from dj-rest-auth social login serializer when utilizing an authorization code
    because of the following issue, https://github.com/iMerica/dj-rest-auth/issues/639

    Should an update to dj-rest-auth, a version > 7.0.0 fix this issue, be sure to remove the
    `serializer_class` attribute of `GoogleLogin` class and leave it as default.
    """
    access_token = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)
    id_token = serializers.CharField(required=False, allow_blank=True)

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        """
        :param adapter: allauth.socialaccount Adapter subclass.
            Usually OAuthAdapter or Auth2Adapter
        :param app: `allauth.socialaccount.SocialApp` instance
        :param token: `allauth.socialaccount.SocialToken` instance
        :param response: Provider's response for OAuth1. Not used in the
        :returns: A populated instance of the
            `allauth.socialaccount.SocialLoginView` instance
        """
        request = self._get_request()
        social_login = adapter.complete_login(
            request, app, token, response=response)
        social_login.token = token
        return social_login

    def set_callback_url(self, view, adapter_class):
        # first set url from view
        self.callback_url = getattr(view, 'callback_url', None)
        if not self.callback_url:
            # auto generate base on adapter and request
            try:
                self.callback_url = reverse(
                    viewname=adapter_class.provider_id + '_callback',
                    request=self._get_request(),
                )
            except NoReverseMatch:
                raise serializers.ValidationError(
                    _('Define callback_url in view'),
                )

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _('View is not defined, pass it as a context variable'),
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(
                _('Define adapter_class in view'))

        adapter = adapter_class(request)
        app = adapter.get_provider().app

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token

        access_token = attrs.get('access_token')
        code = attrs.get('code')
        # Case 1: We received the access_token
        if access_token:
            tokens_to_parse = {'access_token': access_token}
            token = access_token
            # For sign in with apple
            id_token = attrs.get('id_token')
            if id_token:
                tokens_to_parse['id_token'] = id_token

        # Case 2: We received the authorization code
        elif code:
            self.set_callback_url(view=view, adapter_class=adapter_class)
            self.client_class = getattr(view, 'client_class', None)

            if not self.client_class:
                raise serializers.ValidationError(
                    _('Define client_class in view'),
                )

            # Removed Scope from here, as it is not used in the OAuth2 flow
            provider = adapter.get_provider()
            # scope = provider.get_scope_from_request(request)
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                # scope,
                scope_delimiter=adapter.scope_delimiter,
                headers=adapter.headers,
                basic_auth=adapter.basic_auth,
            )
            try:
                token = client.get_access_token(code)
            except OAuth2Error as ex:
                print(ex)
                raise serializers.ValidationError(
                    _('Failed to exchange code for access token')
                ) from ex
            access_token = token['access_token']
            tokens_to_parse = {'access_token': access_token}

            # If available we add additional data to the dictionary
            for key in ['refresh_token', 'id_token', adapter.expires_in_key]:
                if key in token:
                    tokens_to_parse[key] = token[key]
        else:
            raise serializers.ValidationError(
                _('Incorrect input. access_token or code is required.'),
            )

        social_token = adapter.parse_token(tokens_to_parse)
        social_token.app = app

        try:
            if adapter.provider_id == 'google' and not code:
                login = self.get_social_login(
                    adapter, app, social_token, response={'id_token': id_token})
            else:
                login = self.get_social_login(
                    adapter, app, social_token, token)
            ret = complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_('Incorrect value'))

        if isinstance(ret, HttpResponseBadRequest):
            raise serializers.ValidationError(ret.content)

        if not login.is_existing:
            # We have an account already signed up in a different flow
            # with the same email address: raise an exception.
            # This needs to be handled in the frontend. We can not just
            # link up the accounts due to security constraints
            if allauth_account_settings.UNIQUE_EMAIL:
                # Do we have an account already with this email address?
                account_exists = get_user_model().objects.filter(
                    email=login.user.email,
                ).exists()
                if account_exists:
                    raise serializers.ValidationError(
                        _('User is already registered with this e-mail address.'),
                    )

            login.lookup()
            try:
                login.save(request, connect=True)
            except IntegrityError as ex:
                raise serializers.ValidationError(
                    _('User is already registered with this e-mail address.'),
                ) from ex
            self.post_signup(login, attrs)

        attrs['user'] = login.account.user

        return attrs

    def post_signup(self, login, attrs):
        """
        Inject behavior when the user signs up with a social account.

        :param login: The social login instance being registered.
        :type login: allauth.socialaccount.models.SocialLogin
        :param attrs: The attributes of the serializer.
        :type attrs: dict
        """
        pass


class CustomRegisterSerializer(RegisterSerializer):
    def save(self, request):
        user = super().save(request)

        user.username_slug = slugify_username(user.username)

        user.save()

        return user
