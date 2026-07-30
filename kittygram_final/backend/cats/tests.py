from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class CatsAPITestCase(TestCase):
    """Набор тестов для проверки эндпоинтов API котиков."""

    def setUp(self):
        """Подготовить тестового пользователя и авторизованного API-клиента."""
        user = get_user_model()
        self.user = user.objects.create_user(username='auth_user')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_exists(self):
        """Проверить доступность списка задач."""
        response = self.client.get('/api/cats/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
