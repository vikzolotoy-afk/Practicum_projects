from rest_framework.serializers import ValidationError


def username_not_me(value):
    if value.lower() == 'me':
        raise ValidationError("Имя 'me' использовать запрещено.")
    return value
