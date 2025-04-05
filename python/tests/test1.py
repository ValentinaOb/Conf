import unittest
from unittest.mock import MagicMock
import os
import django
import sys

# Налаштувати Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python.settings')
django.setup()

# Додати шлях для імпорту
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from base.views import sign  # твоя функція

class TestUserRegistration(unittest.TestCase):
    def test_successful_registration(self):
        request = MagicMock()
        request.method = "POST"
        request.POST.get.side_effect = lambda key, default="": {
            "username": "testuser",
            "email": "test@mail.com",
            "password": "test1234"
        }.get(key, default)

        response = sign(request)
        
        # Перевірка статусу після перенаправлення
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'home')

    def test_already_taken_username_registration(self):
        request = MagicMock()
        request.method = "POST"
        request.POST.get.side_effect = lambda key, default="": {
            "username": "testuser",
            "email": "test1@mail.com",
            "password": "test1234"
        }.get(key, default)

        response = sign(request)
        
        # Перевірка статусу після перенаправлення
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'home')


    def test_missing_username(self):
        request = MagicMock()
        request.POST.get.side_effect = lambda key, default="": {
            "email": "test@mail",
            "password": "test1234"
        }.get(key, default)

        response = sign(request)
        self.assertEqual(response.status_code, 400)

    def test_missing_email(self):
        request = MagicMock()
        request.POST.get.side_effect = lambda key, default="": {
            "username": "testuser",
            "password": "test1234"
        }.get(key, default)

        response = sign(request)
        self.assertEqual(response.status_code, 400)

    def test_missing_password(self):
        request = MagicMock()
        request.POST.get.side_effect = lambda key, default="": {
            "username": "testuser",
            "email": "test@mail"
        }.get(key, default)

        response = sign(request)
        self.assertEqual(response.status_code, 400)

    def test_incorrect_password_format(self):
        request = MagicMock()
        request.POST.get.side_effect = lambda key, default="": {
            "username": "testuser",
            "email": "test@mail",
            "password": "12345678"
        }.get(key, default)

        response = sign(request)
        self.assertEqual(response.status_code, 400)



if __name__ == '__main__':
    unittest.main()
