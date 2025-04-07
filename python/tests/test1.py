import unittest
from unittest.mock import MagicMock
import os
import django
import sys
from django.urls import reverse
from django.test import TestCase
#unittest.TestLoader.sortTestMethodsUsing = None

# Налаштувати Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python.settings')
django.setup()
from django.contrib.auth.models import User
# Додати шлях для імпорту
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from django.contrib.auth.models import User
from django.test import Client
from base.models import Work, User_Data
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


class TestUserUpload_Profile(TestCase): 
    @classmethod

    @classmethod
    def setUpClass(cls):
        super(TestUserUpload_Profile, cls).setUpClass()
        cls.client = Client()

    def setUp(self):
        User.objects.filter(username="testuser").delete()
        self.email = 'oldemail@example.com'
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email=self.email
        )
        login_success = self.client.login(username="testuser", password="testpassword123")
        self.assertTrue(login_success, "User failed to login during setUp")

        User_Data.objects.filter(user=self.user).delete()

        self.user_data = User_Data.objects.create(
            user=self.user,
            firstname='testname',
            lastname='testlast',
            phone='0000000000',
            job='testjob',
            country='ukraine',
            language='ukrainian',
        )

    def tearDown(self):
        User.objects.filter(username__in=['testuser', 'newtest']).delete()

    def test_home(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile(self):

        response = self.client.get('/user_profile/')
        self.assertEqual(response.status_code, 200)
        
    def test_edit_profile(self):
        response = self.client.post(reverse('edit_profile'), {
            'firstname':'testname',
            'lastname':'testlast',
            'phone':'0000000000',
            'job':'testjob',
            'country':'ukraine',
            'language':'ukrainian',
            'email': 'newemail@example.com',
            'username':'newtest'            
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual({self.user_data.firstname,self.user_data.lastname,self.user_data.phone,self.user_data.job,self.user_data.country,self.user_data.language, self.user.email,self.user.username}, 
                         {'testname','testlast','0000000000','testjob','ukraine','ukrainian','newemail@example.com'})

    def test_deactivate_account(self):
        response = self.client.post(f'/deactivate_account{self.id}')
        '''self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user.is_active)'''
        self.assertEqual(response.status_code, 302)

    def test_password_reset_request(self):
        # Перевіримо, чи лист згенеровано
        from django.core import mail
        response = self.client.post(reverse('password_reset'), {'email': self.email})
        self.assertEqual(response.status_code, 302)  # redirect to 'done' page
        self.assertEqual(len(mail.outbox), 1)  # Exactly one email sent
        self.assertIn(self.email, mail.outbox[0].to)

    def test_change_password(self):#
        response = self.client.post(reverse('change_password'), {
            'old_password': 'testpassword123',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456',
        })
        self.assertEqual(response.status_code, 302)  # редірект після зміни пароля

        # Вийдемо і залогінемося з новим паролем
        self.client.logout()
        login_successful = self.client.login(username='testuser', password='newpassword456')
        self.assertTrue(login_successful)





'''    def test_admin_page_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/admin/')  # URL сторінки адміністратора за замовченням
        self.assertEqual(response.status_code, 200)'''


if __name__ == '__main__':
    unittest.main()
