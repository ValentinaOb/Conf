from django.db import models
import os, datetime
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth import get_user_model

class Work (models.Model):
    #id = models.AutoField(primary_key=True)
    category = models.TextField(null=False)
    title = models.TextField(null=False)
    authors = models.TextField(null=False)
    file = models.FileField(upload_to='files/', null=True, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size=models.IntegerField(null=False)

    class WorkStatus(models.TextChoices):
        Send='send'
        Review='review'
        Accept='accept'
        Refuse='refuse'

    status= models.CharField(max_length=15,null=False, choices=WorkStatus.choices, default='Send')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

class User_Data (models.Model):
    firstname = models.TextField(null=True)
    lastname = models.TextField(null=True)
    job = models.TextField(null=True)
    phone = PhoneNumberField(null=True)
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.png', null=True, blank=True)
    country = models.TextField(null=True)
    language = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if not self.avatar:  # ✅ If img is empty, set the default
            self.avatar = "avatars/default.png"
        super().save(*args, **kwargs)


from django.forms import ModelForm

class UploadWorkForm(ModelForm):
    class Meta:
        model = Work
        fields = ['category','title','authors', 'file', 'file_size', 'user']

class UploadUserDataForm(ModelForm):
    class Meta:
        model = User_Data
        fields = ['firstname','lastname', 'job', 'phone', 'avatar', 'country', 'language', 'user']



'''class UserManager(Manager):
    def get_queryset(self):
        return User.objects.filter(user=self.request.user)'''