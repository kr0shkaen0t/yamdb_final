from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value < 1500 or value > timezone.now().year:
        raise ValidationError(
            ('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
