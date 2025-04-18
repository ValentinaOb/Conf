import unittest
from unittest.mock import MagicMock
import os
import django
import sys
from django.urls import reverse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.conf import settings

#unittest.TestLoader.sortTestMethodsUsing = None

# Налаштувати Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python.settings')
django.setup()
from django.contrib.auth.models import User
# Додати шлях для імпорту
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from django.contrib.auth.models import User
from django.test import Client
from base.models import Work, User_Data,User_Role,Review_Work
#response = '/sign/'(request)
from django.core import mail
from django.test import override_settings
import time
class TestUserRegistration(unittest.TestCase): 
    @classmethod
    def setUpClass(cls):
        super(TestUserRegistration, cls).setUpClass()
        cls.client = Client()

    def setUp(self):
        User.objects.filter(email__in=['oldemail@example.com','test@mail.com', 'new@mail.com']).delete()
        self.email = 'oldemail@example.com'
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email=self.email
        )
        login_success = self.client.login(username="testuser", password="testpassword123")
        self.assertTrue(login_success, "User failed to login during setUp")               

    def test_successful_registration(self):
        start_time = time.time()
        response = self.client.post('/sign/', {
            'username': 'testuser1',
            'email': 'test@mail.com',
            'password': 'test1234'
        })
        self.assertEqual(response.status_code, 302)  # Редірект на home
        end_time = time.time()
        duration = end_time - start_time
        print(f"Reg/Response time: {duration:.4f} seconds")

    def test_already_taken_email_registration(self):
        response = self.client.post('/sign/', {
            'username': 'newuser',
            'email': 'oldemail@example.com',  # вже зайнятий email
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, 400)  # Очікуємо 400 через існуючий email

    def test_already_taken_username_registration(self):
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
        User.objects.filter(email__in=['oldemail@example.com','test@mail.com']).delete()
        #User.objects.filter(username="testuser").delete()
        self.email = 'oldemail@example.com'
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email=self.email
        )
        login_success = self.client.login(username="testuser", password="testpassword123")
        self.assertTrue(login_success, "User failed to login during setUp")     

    def test_successful_login(self):
        response = self.client.post('/login/', {
            'email': 'oldemail@example.com',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Редірект на home

    def test_incorrect_email(self):
        response = self.client.post('/login/', {
            'email': 'test@mail.com', 
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_incorrect_pswd(self):
        response = self.client.post('/login/', {
            'email': 'oldemail@example.com', 
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 400) 

    def test_successful_logout(self):
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



@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TestUserUpload_Profile(TestCase): 
    @classmethod
    def setUpClass(cls):
        super(TestUserUpload_Profile, cls).setUpClass()
        cls.client = Client()

    def setUp(self):
        User.objects.filter(email__in=['oldemail@example.com','test@mail.com']).delete()
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
        User_Role.objects.filter(user=self.user).delete()

        self.user_role = User_Role.objects.create(
            user=self.user,
            user_role='user',
        )

        Work.objects.filter(user=self.user).delete()
        
        self.file = SimpleUploadedFile(
            name="document.txt",
            content=b"Some content here",
            content_type="text/plain"
        )
        self.work = Work.objects.create(
            user=self.user,
            category='computer_science',
            title= 'maintitle',
            authors= 'testauthors',
            file=self.file,
            file_size=self.file.size
        )
        
        file_path = os.path.join(settings.MEDIA_ROOT, 'files', self.work.title)
        if os.path.isfile(file_path):
            os.remove(file_path)

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
                         {'testname','testlast','0000000000','testjob','ukraine','ukrainian','newemail@example.com','newtest'})
  
    def test_deactivate_account(self):
        response = self.client.post(f'/deactivate_account/{self.user.id}')
        self.assertEqual(response.status_code, 302)
         
    def test_password_reset_request(self):
        start_time = time.time()
        response = self.client.post(reverse('password_reset'), {'email': 'oldemail@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password reset', mail.outbox[0].subject)
        end_time = time.time()
        duration = end_time - start_time
        print(f"E/Response time: {duration:.4f} seconds")

    def test_change_password(self):
        response = self.client.post(reverse('change_password'), {
            'old_password': 'testpassword123',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456',
        })
        self.assertEqual(response.status_code, 302)  # редірект після зміни пароля

        # Вийдемо і логінемося з новим паролем
        self.client.logout()
        login_successful = self.client.login(username='testuser', password='newpassword456')
        self.assertTrue(login_successful)
         
    def test_valid_file_upload(self):
        self.file = SimpleUploadedFile(
            name="document.txt",
            content=b"Some content here",
            content_type="text/plain"
        )

        response = self.client.post(reverse('upload'), {
            'category': 'computer_science',
            'title': 'testtitle',
            'authors': 'testauthors',
            'file': self.file,
            'file_size': self.file.size,
            'user': self.user,
        })
        self.assertEqual(response.status_code, 302)
    
    def test_file_upload_already_use_title(self):
        #print('W ',Work.objects.values('title').last())
        #self.assertEqual(User.objects.count(), 6)
        self.file = SimpleUploadedFile(
            name="document.txt",
            content=b"Some content here",
            content_type="text/plain"
        )
        response = self.client.post(reverse('upload'), {
            'category': 'computer_science',
            'title': 'maintitle',
            'authors': 'testauthors',
            'file': self.file,
            'file_size': self.file.size,
            'user': self.user,
        })
        self.assertEqual(response.status_code, 400)

    def test_valid_file_update(self):
        start_time = time.time()
        response = self.client.post(f'/update/{self.work.id}', {
            'updaterecord': '1',
            'category': 'mathematics',
            'title': 'newtitle',
            'authors': 'testauthor, author',
            'file': self.file,
            'file_size': self.file.size,
            'user': self.user,
        })
        self.assertEqual(response.status_code, 302)
        self.work.refresh_from_db()
        self.assertEqual({self.work.category,self.work.title,self.work.authors,self.work.file_size},
                         {'mathematics','newtitle','testauthor, author',self.file.size})
        end_time = time.time()
        duration = end_time - start_time
        print(f"Upl/Response time: {duration:.4f} seconds")

    def test_valid_file_delete(self):
        response = self.client.post(f'/delete/{self.work.id}')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Delete", str(messages[0]))

    def test_errorr_file_delete(self):
        response = self.client.post(f'/delete/{self.work.id+100}')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Error", str(messages[0]))

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TestAdmin(TestCase): 
    @classmethod
    def setUpClass(cls):
        super(TestAdmin, cls).setUpClass()
        cls.client = Client()

    def setUp(self):
        self.email = 'oldemail@example.com'
        self.rev_email = 'test@mail.com'
        self.rev1_email = 'rev_test@mail.com'
        User.objects.filter(email__in=[self.email,self.rev_email,self.rev1_email]).delete()
        
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email=self.email
        )
        login_success = self.client.login(username="testuser", password="testpassword123")
        self.assertTrue(login_success, "User failed to login during setUp")

        self.user_data = User_Data.objects.create(
            user=self.user,
            firstname='testname',
            lastname='testlast',
            phone='0000000000',
            job='testjob',
            country='ukraine',
            language='ukrainian',
        )
        
        #reviewer
        self.rev_user = User.objects.create_user(
            username="reviewertestuser",
            password="test123",
            email=self.email
        )
        login_success = self.client.login(username="reviewertestuser", password="test123")
        self.assertTrue(login_success, "User failed to login during setUp")

        #reviewer1
        self.rev1_user = User.objects.create_user(
            username="reviewer1_testuser",
            password="test123",
            email=self.email
        )
        login_success = self.client.login(username="reviewer1_testuser", password="test123")
        self.assertTrue(login_success, "User failed to login during setUp")

        
        User_Data.objects.filter(user__in={self.user,self.rev_user,self.rev1_user}).delete()
        User_Role.objects.filter(user__in={self.user,self.rev_user,self.rev1_user}).delete()
        Work.objects.filter(user__in={self.user,self.rev_user,self.rev1_user}).delete()

        self.user_role = User_Role.objects.create(
            user=self.user,
            user_role='admin',
        )

        self.file = SimpleUploadedFile(
            name="document.txt",
            content=b"Some content here",
            content_type="text/plain"
        )

        self.work = Work.objects.create(
            user=self.user,
            category='computer_science',
            title= 'maintitle',
            authors= 'testauthors',
            file=self.file,
            file_size=self.file.size
        )
        self.work1 = Work.objects.create(
            user=self.user,
            category='mathematics',
            title= 'subtitle',
            authors= 'newauthors',
            file=self.file,
            file_size=self.file.size
        )

        for filename in {self.work.title,self.work1.title}:
            file_path = os.path.join(settings.MEDIA_ROOT, 'files', filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        self.rev_user_role = User_Role.objects.create(
            user=self.rev_user,
            user_role='reviewer',
        )
        
        self.rev_user_data = User_Data.objects.create(
            user=self.user,
            firstname='testna',
            lastname='Revtestlast',
            phone='000006789',
            job='testjob',
            country='ukraine',
            language='ukrainian',
        )

        self.rev1_user_role = User_Role.objects.create(
            user=self.rev1_user,
            user_role='reviewer',
        )

        self.rev1_user_data = User_Data.objects.create(
            user=self.user,
            firstname='testnam',
            lastname='Rtestlast',
            phone='012345789',
            job='testjob',
            country='ukraine',
            language='ukrainian',
        )


    def test_admin_home(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/admin/home/')
        self.assertEqual(response.status_code, 302)
    
    def test_valid_to_review_one(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/to_review/{self.work.id}',{
            'title':self.work.title,
            'reviewer':self.rev1_user.id
        })
        self.assertEqual(response.status_code, 302)

    def test_valid_to_review_two(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/to_review/{self.work.id}',{
            'title':self.work.title,
            'reviewer':{self.rev_user.id,self.rev1_user.id}
        })
        self.assertEqual(response.status_code, 302)

    def test_valid_email_send_one(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/email_send/',{
            'email': '1',
            'selected_works':self.work.id,
            'work_status': 'accept'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('oldemail@example.com', mail.outbox[0].to)

    def test_valid_email_send_two(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/email_send/',{
            'email': '1',
            'selected_works':{self.work.id,self.work1.id},
            'work_status': 'accept'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 2)
        

    def test_valid_description_without(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/email_send/',{
            'description': '1'
        })
        self.assertEqual(response.status_code, 302)

    def test_valid_admin_description_one(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/email_send/',{
            'description': '1',
            'work':self.work.id
        })
        self.assertEqual(response.status_code, 302)

    def test_valid_admin_description_two(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/email_send/',{
            'description': '1',
            'work':{self.work.id, self.work1.id}
        })
        self.assertEqual(response.status_code, 302)

    def test_valid_assign_role_one(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/assign_role/',{
            'selected_users': self.rev1_user.id,
            'user_role':'admin'
        })
        self.rev1_user_role.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.rev1_user_role.user_role,'admin')

    def test_valid_assign_role_two(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/admin/assign_role/',{
            'selected_users': {self.rev1_user.id, self.rev_user.id},
            'user_role':'user'
        })
        self.rev_user_role.refresh_from_db()
        self.rev1_user_role.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual({self.rev_user_role.user_role,self.rev1_user_role.user_role},{'user','user'})

    
class TestReviewer(TestCase): 
    @classmethod
    def setUpClass(cls):
        super(TestReviewer, cls).setUpClass()
        cls.client = Client()

    def setUp(self):
        self.email = 'oldemail@example.com'
        self.rev_email = 'test@mail.com'
        self.rev1_email = 'rev_test@mail.com'
        User.objects.filter(email__in=[self.email,self.rev1_email,self.rev_email]).delete()
        
        self.rev_user = User.objects.create_user(
            username="rev_testuser",
            password="testpassword123",
            email=self.rev1_email
        )
        login_success = self.client.login(username="rev_testuser", password="testpassword123")
        self.assertTrue(login_success, "User failed to login during setUp")

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email=self.email
        )
        login_success = self.client.login(username="testuser", password="testpassword123")
        self.assertTrue(login_success, "User failed to login during setUp")

        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword123",
            email=self.rev_email
        )
        login_success = self.client.login(username="testuser1", password="testpassword123")
        self.assertTrue(login_success, "User failed to login during setUp")

        self.user_data = User_Data.objects.create(
            user=self.user,
            firstname='testname',
            lastname='testlast',
            phone='0000000000',
            job='testjob',
            country='ukraine',
            language='ukrainian',
        )
        
        User_Data.objects.filter(user__in={self.user,self.rev_user}).delete()
        User_Role.objects.filter(user__in={self.user,self.rev_user}).delete()
        Work.objects.filter(user__in={self.user,self.rev_user}).delete()
        Review_Work.objects.filter(user__in={self.user,self.rev_user}).delete()

        self.user_role = User_Role.objects.create(
            user=self.user,
            user_role='reviewer',
        )

        self.file = SimpleUploadedFile(
            name="document.txt",
            content=b"Some content here",
            content_type="text/plain"
        )

        self.work = Work.objects.create(
            user=self.user,
            category='computer_science',
            title= 'maintitle',
            authors= 'testauthors',
            file=self.file,
            file_size=self.file.size
        )
        self.work1 = Work.objects.create(
            user=self.user1,
            category='mathematics',
            title= 'subtitle',
            authors= 'newauthors',
            file=self.file,
            file_size=self.file.size
        )

        self.rev_work=Review_Work.objects.create(
            user=self.user,
            work=self.work
        )
        self.rev_work1=Review_Work.objects.create(
            user=self.user,
            work=self.work1
        )

        for filename in {self.work.title,self.work1.title}:
            file_path = os.path.join(settings.MEDIA_ROOT, 'files', filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_reviewer_home(self):
        self.client.login(username='rev_testuser', password='testpassword123')
        response = self.client.get('/reviewer/home')
        self.assertEqual(response.status_code, 200)
        
    def test_valid_review_status(self):
        start_time = time.time()
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/reviewer/review_status/{self.work1.id}',{
            'work_status': 'accept',
            'feedback':'Good work',
            'title':self.work1.title
        })        
        self.assertEqual(response.status_code, 302)
        self.rev_work1.refresh_from_db()
        self.assertEqual({self.rev_work1.status,self.rev_work1.description}, {'accept','Good work'})
        end_time = time.time()
        duration = end_time - start_time
        print(f"St/Response time: {duration:.4f} seconds")
        
    def test_valid_description_one(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/reviewer/view_description/',{
            'selected_works':self.work.id
        },follow=True)        
        self.assertEqual(response.status_code, 200)

    def test_valid_description_two(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/reviewer/view_description/',{
            'selected_works':{self.work.id,self.work1.id}
        },follow=True)        
        self.assertEqual(response.status_code, 200)

    def test_valid_review_file(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(f'/reviewer/review_file/{self.work.id}')        
        self.assertEqual(response.status_code, 200)   

if __name__ == '__main__':
    unittest.main()
