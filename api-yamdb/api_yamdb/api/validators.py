from rest_framework import serializers


def validate_not_empty(value):
    """Валидатор для проверки на пустоту и пробелы."""
    if not value or not value.strip():
        raise serializers.ValidationError('Поле не может быть пустым.')
    return value
