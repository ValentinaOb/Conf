# Generated by Django 5.1.4 on 2025-03-29 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_review_work_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review_work',
            name='user',
            field=models.TextField(null=True),
        ),
    ]
