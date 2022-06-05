from django.conf import settings
from rest_framework import serializers


def validate_username(self, value):
    if value.lower() == settings.USER_ME:
        raise serializers.ValidationError(
            'Для имени нельзя использовать {value}'
        )
    return value
