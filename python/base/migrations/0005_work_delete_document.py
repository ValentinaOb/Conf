# Generated by Django 5.1.4 on 2025-01-27 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_document_user_alter_document_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField()),
                ('title', models.TextField()),
                ('authors', models.TextField()),
                ('file', models.FileField(null=True, upload_to='files/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file_size', models.IntegerField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
