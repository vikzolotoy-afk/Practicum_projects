"""Функции импорта CSV файлов."""
import csv

from django.db import models


def get_field_value(field, row):
    field_name = field.name
    csv_value = row.get(field_name) or row.get(f"{field_name}_id")

    value = csv_value.strip() if csv_value is not None else None

    if value in ('', None):
        if isinstance(field, (models.CharField, models.TextField)):
            return ''
        else:
            return None

    if isinstance(field, models.ForeignKey):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    return value


def import_csv(file_path, model_class):
    """
    Универсальный импорт CSV в любую модель Django.
    Работает с ForeignKey через field_id.
    """
    objs = []

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            row_data = {}

            for field in model_class._meta.fields:
                value = get_field_value(field, row)

                if value is None:
                    if field.has_default():
                        value = field.get_default()
                    elif isinstance(field, models.BooleanField):
                        value = False
                    elif not field.null:
                        if isinstance(field, models.CharField):
                            value = ''
                        else:
                            raise ValueError(
                                f"Не удалось импортировать поле {field.name}. "
                                "Нет значения и нет default."
                            )
                if isinstance(field, models.ForeignKey):
                    row_data[f'{field.name}_id'] = value
                else:
                    row_data[field.name] = value

            objs.append(model_class(**row_data))

    model_class.objects.bulk_create(objs)


def import_title_genres(file_path):
    """
    Импорт жанров для каждого Title из CSV genre_title.csv.

    CSV содержит колонки: title_id, genre_id
    """
    from reviews.models import Title, Genre

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])
            title.genre.add(genre)
