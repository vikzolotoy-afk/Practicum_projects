from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_year(value):
    current_year = now().year
    if value > current_year:
        raise ValidationError(
            f'Год выпуска не может быть больше {current_year}')
