# Generated by Django 3.0.1 on 2019-12-30 11:45

from django.db import migrations, models
import modules.files_manager.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название файла')),
                ('attachments', models.FileField(blank=True, upload_to=modules.files_manager.models.path_file, verbose_name='Файлы')),
            ],
        ),
    ]