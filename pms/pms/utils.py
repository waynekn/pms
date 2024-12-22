import re

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
