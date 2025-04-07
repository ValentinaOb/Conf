import unittest
from unittest.mock import MagicMock
import os
import django
import sys
from django.urls import reverse
#unittest.TestLoader.sortTestMethodsUsing = None

# Налаштувати Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python.settings')
django.setup()
from django.contrib.auth.models import User
# Додати шлях для імпорту
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from django.contrib.auth.models import User
from django.test import Client
#response = '/sign/'(request)

class TestUserRegistration(unittest.TestCase): 
    @classmethod
    def setUpClass(cls):
        super(TestUserRegistration, cls).setUpClass()
        cls.client = Client()

    def setUp(self):
        User.objects.filter(username__in=['testuser', 'anotheruser']).delete()
        User.objects.filter(email__in=['test@mail.com', 'test1@mail.com']).delete()

    def test_successful_registration(self):
        response = self.client.post('/sign/', {
            'username': 'testuser',
            'email': 'test@mail.com',
            'password': 'test1234'
        })
        self.assertEqual(response.status_code, 302)  # Редірект на home

    def test_already_taken_email_registration(self):
        User.objects.create_user(username='anotheruser', email='test@mail.com', password='test1234')

        response = self.client.post('/sign/', {
            'username': 'newuser',
            'email': 'test@mail.com',  # вже зайнятий email
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, 400)  # Очікуємо 400 через існуючий email

    def test_already_taken_username_registration(self):
        User.objects.create_user(username='testuser', email='other@mail.com', password='test1234')

        response = self.client.post('/sign/', {
            'username': 'testuser',  # вже зайняте ім'я
            'email': 'new@mail.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 400)  # Очікуємо 400 через існуюче ім'я

'''    def test_missing_username(self):
        request = MagicMock()
        request.POST.get.side_effect = lambda key, default="": {
            "email": "test@mail",
            "password": "test1234"
        }.get(key, default)

        response = '/sign/'(request)
        self.assertEqual(response.status_code, 400)

    def test_incorrect_password_format(self):
        request = MagicMock()
        request.POST.get.side_effect = lambda key, default="": {
            "username": "testuser",
            "email": "test@mail",
            "password": "12345678"
        }.get(key, default)

        response = '/sign/'(request)
        self.assertEqual(response.status_code, 400)

'''

class TestUserLogIn_Out(unittest.TestCase): 
    @classmethod
    def setUpClass(cls):
        super(TestUserLogIn_Out, cls).setUpClass()
        cls.client = Client()

    def setUp(self):
        User.objects.filter(username__in=['testuser', 'anotheruser']).delete()
        User.objects.filter(email__in=['test@mail.com', 'test1@mail.com']).delete()

    def test_successful_login(self):
        User.objects.create_user(username='anotheruser', email='test@mail.com', password='test1234')

        response = self.client.post('/login/', {
            'email': 'test@mail.com',
            'password': 'test1234'
        })
        self.assertEqual(response.status_code, 302)  # Редірект на home

    def test_incorrect_email(self):
        User.objects.create_user(username='anotheruser', email='test@mail.com', password='test1234')

        response = self.client.post('/login/', {
            'email': 'test1@mail.com', 
            'password': 'test1234'
        })
        self.assertEqual(response.status_code, 400) 

    def test_successful_logout(self):
        User.objects.create_user(username='anotheruser', email='test@mail.com', password='test1234')

        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 302) 


class TestUserGeneral(unittest.TestCase): 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_index_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_committee_page(self):
        response = self.client.get('/committee/')
        self.assertEqual(response.status_code, 200)

    def test_schedule_page(self):
        response = self.client.get('/schedule/')
        self.assertEqual(response.status_code, 200)
    
    def test_contact_page(self):
        response = self.client.get(reverse('committee'))
        self.assertEqual(response.status_code, 200)
    
    def test_404_page(self):
        response = self.client.get('/some/nonexistent/page/')
        self.assertEqual(response.status_code, 404)


class TestUserUpload_Profile(unittest.TestCase): 
    @classmethod
    def setUpClass(cls):
        super(TestUserLogIn_Out, cls).setUpClass()
        cls.client = Client()



'''    def test_admin_page_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/admin/')  # URL сторінки адміністратора за замовченням
        self.assertEqual(response.status_code, 200)'''


if __name__ == '__main__':
    unittest.main()
