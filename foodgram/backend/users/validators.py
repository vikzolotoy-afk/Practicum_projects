import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверить имя пользователя на запрещенные слова и символы."""
    if value.lower() == "me":
        raise ValidationError('Использовать имя "me" запрещено.')
    if not re.match(r"^[\w.@+-]+\Z", value):
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы.'
        )
    return value
