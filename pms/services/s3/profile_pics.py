import logging
from django.conf import settings
from django.core.cache import cache
from django.core.files import File
from botocore.exceptions import ClientError

from .client import s3_client
from services.utils.image_processing import process_profile_pic


def upload_profile_pic(picture: File, picture_name: str) -> bool:
    """
    Upload an picture to an S3 bucket

    params:
        - param picture: File to upload
        - param picture_name: S3 object name.
        - return: True if file was uploaded, else False
    """
    BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

    img_buffer = process_profile_pic(picture)

    picture_name = "profile-pics/" + picture_name
    DEFAULTPROFILEPICTURE = "profile-pics/" + settings.DEFAULT_PROFILE_PICTURE

    try:
        s3_client.upload_fileobj(img_buffer, BUCKET_NAME, picture_name)

        if picture_name != DEFAULTPROFILEPICTURE:
            cache.delete(picture_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_profile_pic_url(picture_name) -> str:
    """
    Generate a presigned URL to share an S3 object

    params:
        - param picture_name: string
        - return: Presigned URL as string. If error, returns an empty string.
    """
    BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
    EXPIRATION = 3600  # 1hour
    TIMEOUT = 59.5 * 60  # 59.5 minutes
    picture_name = "profile-pics/" + picture_name

    cached_url = cache.get(picture_name)

    if cached_url:
        return cached_url

    try:
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': BUCKET_NAME,
                                                       'Key': picture_name},
                                               ExpiresIn=EXPIRATION)
        cache.set(picture_name, url, timeout=TIMEOUT)
    except ClientError as e:
        logging.error(e)
        return ""

    return url


def delete_profile_pic(picture_name: str) -> bool:
    """
    Delete a profile picture

    params:
        - picture_name: Name of the picture to delete (relative key without prefix).
        - return: True if deleted successfully, False otherwise.
    """
    BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
    picture_name = "profile-pics/" + picture_name

    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=picture_name)
        return True
    except ClientError as e:
        logging.error(e)
        return False
