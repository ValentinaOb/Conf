# Generated by Django 5.1.4 on 2025-03-26 16:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_alter_work_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rewiev_Work',
            new_name='Review_Work',
        ),
    ]
