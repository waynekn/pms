import os
import re
from dotenv import load_dotenv
from django.core.exceptions import ValidationError
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import SocialLoginSerializer, UserDetailsSerializer
from .models import User
from .validators import username_validator
from .utils import slugify_username
from services.s3.profile_pics import upload_profile_pic

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
