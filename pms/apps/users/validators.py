from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

username_validator = RegexValidator(
    regex=r'^[\w.@+-]+(?: [\w.@+-]+)*\Z',
    message=_(
        'Enter a valid username. This value may contain only letters, numbers, '
        'and @/./+/-/_ characters, with a single space allowed between words.'
    ),
    code='invalid'
)
