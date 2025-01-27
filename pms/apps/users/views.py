import os
import re

from dotenv import load_dotenv
from django.core.exceptions import ValidationError
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import SocialLoginSerializer, UserDetailsSerializer
from .models import User
from .validators import username_validator
from .utils import slugify_username
from services.s3.profile_pics import upload_profile_pic, delete_profile_pic

load_dotenv()

# Create your views here.


class AccountRegsitrationView(RegisterView):
    """
    Handle user registration and set authentication tokens as cookies.

    This view extends the `RegisterView` from `dj-rest-auth` to customize
    the response by setting the access and refresh tokens as HTTP-only cookies.
    By default, `dj-rest-auth` does not set these tokens as cookies during registration.
    """

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(request)
            user_response = UserDetailsSerializer(user).data
            response = Response(user_response,
                                status=status.HTTP_201_CREATED)

            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            response.set_cookie(
                key='access_token',
                value=str(access),
                httponly=True,
                samesite='Lax',
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                samesite='Lax',
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    """
    Handle Google auth using Authorization Code Grant
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.getenv('GOOGLE_REDIRECT_URL')
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


class UserProfilePictureUpdateView(generics.UpdateAPIView):
    """
    Handle updating user's profile picture
    """

    def put(self, request: Request, *args, **kwargs) -> Response:
        uploaded_file = request.data.get('avatar')
        IMAGE_EXTS = r'(jpg|jpeg|png)$'
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

        if not uploaded_file:
            return Response({"detail": "No image was provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        if uploaded_file.size > MAX_FILE_SIZE:
            return Response({
                "detail": "The uploaded file is too large. It must be 5MB or less"
            }, status=status.HTTP_400_BAD_REQUEST)

        file_mimetype = uploaded_file.content_type
        file_ext = file_mimetype.split('/')[1]

        if (not re.match(IMAGE_EXTS, file_ext)):
            return Response({"detail": "Invalid file type. Only .jpg, .jpeg or .png are allowed"},
                            status=status.HTTP_400_BAD_REQUEST)

        successful = upload_profile_pic(
            uploaded_file, str(request.user.user_id))

        if not successful:
            return Response({'detail': 'An error occurred while uploading the image'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user: User = self.request.user
        user.profile_picture = str(user.pk)
        user.save()

        updated_user = UserDetailsSerializer(user)

        return Response(updated_user.data, status=status.HTTP_200_OK)


class UsernameUpdateView(generics.UpdateAPIView):
    """
    View to updata a users username.

    This view also converts the username to a slug and saves it to the user's profile.
    """

    def put(self, request: Request, *args, **kwargs) -> Response:
        username = request.data.get('username')

        if not username:
            return Response({'detail': 'No username was provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        username = username.strip()

        try:
            username_validator(username)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(username=username)
            return Response({'detail': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        slug = slugify_username(username)

        user: User = request.user
        user.username = username
        user.username_slug = slug
        user.save()

        return Response(UserDetailsSerializer(user).data, status=status.HTTP_200_OK)


class UserAccountDeleteView(generics.DestroyAPIView):
    """
    Handles requests to delete a user's account, including optional
    cleanup of their profile picture if it is custom.
    """

    def delete(self, request: Request, *args, **kwargs) -> Response:
        user: User = request.user

        # if the profile picture is the stringified user_id, then that means
        # they had a custom profile picture
        if user.profile_picture == str(user.pk):
            deleted = delete_profile_pic(user.profile_picture)

            if not deleted:
                return Response({'detail': 'An error occurred while deleting your account. Please try again later'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user.delete()

        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('sessionid')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
