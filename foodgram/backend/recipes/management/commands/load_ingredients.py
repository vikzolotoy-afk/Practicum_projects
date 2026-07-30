import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из JSON файла'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(settings.BASE_DIR.parent, 'data')
        path = os.path.join(data_dir, 'ingredients.json')

        self.stdout.write(f'Ищу файл по адресу: {path}')

        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR('Файл не найден!'))
            return

        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            Ingredient.objects.bulk_create(
                (Ingredient(**item) for item in data),
                ignore_conflicts=True
            )

            self.stdout.write(
                self.style.SUCCESS('Ингредиенты успешно загружены!')
            )

        except (OSError, json.JSONDecodeError) as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка чтения или парсинга файла: {e}')
            )
        except (TypeError, KeyError) as e:
            self.stdout.write(
                self.style.ERROR(f'Данные в JSON не соответствуют модели: {e}')
            )
