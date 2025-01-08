import re
import uuid
import string


pattern = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(name):
    """
    Converts a camelCase string to snake_case.
    """
    return pattern.sub('_', name).lower()


def camel_case_to_snake_case(data):
    """
    Recursively goes through the data and converts all keys from camelCase to snake_case.
    """
    if isinstance(data, dict):
        return {camel_to_snake(key): camel_case_to_snake_case(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [camel_case_to_snake_case(item) for item in data]
    else:
        return data


BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase


def _to_base62(num):
    """Convert an integer to a base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]

    base62 = []
    while num > 0:
        base62.append(BASE62_ALPHABET[num % 62])
        num //= 62

    return ''.join(reversed(base62))[:11]


def base_62_pk():
    """Convert a UUID object to a base62-encoded string."""
    uuid_obj = uuid.uuid4()
    return _to_base62(uuid_obj.int)
