import re

from django.core.exceptions import ValidationError


def validate_slug(value):
    """Проверить строку на соответствие разрешенным символам слага."""
    if not re.match(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError('Слаг содержит недопустимые символы.')
    return value
