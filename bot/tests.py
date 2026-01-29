from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import TelegramUser


class TelegramUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_new_user(self):
        """Регистрация нового пользователя возвращает 201."""
        response = self.client.post(
            "/api/register/",
            {"user_id": 123456, "username": "testuser"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_id"], 123456)

    def test_register_existing_user(self):
        """Повторная регистрация возвращает 200 и already_registered."""
        TelegramUser.objects.create(user_id=123456, username="testuser")
        response = self.client.post(
            "/api/register/",
            {"user_id": 123456, "username": "testuser"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("already_registered"))

    def test_get_existing_user(self):
        """Получение существующего пользователя возвращает 200."""
        TelegramUser.objects.create(user_id=123456, username="testuser")
        response = self.client.get("/api/user/123456/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_get_nonexistent_user(self):
        """Получение несуществующего пользователя возвращает 404."""
        response = self.client.get("/api/user/999999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "User not found")
