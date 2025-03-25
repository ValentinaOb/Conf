from django.test import TestCase

from .models import User, User_Data

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="username", email="email@gmail", password="password1")

class UserDataModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User_Data.objects.create(firstname='firstname',lastname='lastname',phone='00000000000',job='job',
                avatar='',country='country',language='language',user=User)
    
    def setUpTestData(cls):
        User_Data.objects.create(firstname='firstname',lastname='lastname',phone='00000000000',job='job',
                avatar='',country='country',language='language',user=User)
    
class WebAppTests(TestCase):
    
    def test_main_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')
        
    def test_home_page(self):
        response = self.client.get('home')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')

    def test_about_page(self):
        response = self.client.get('about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
        
    def test_committee_page(self):
        response = self.client.get('committee/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Committee')

    def test_schedule_page(self):
        response = self.client.get('schedule/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Schedule')

    def test_contact_page(self):
        response = self.client.get('contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact')
        
    def test_sign_page(self):
        response = self.client.get('sign/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign')
    
    def test_404_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)
    
    def test_static_files(self):
        response = self.client.get('/static/css/style.css')
        self.assertIn(response.status_code, [200, 304])

