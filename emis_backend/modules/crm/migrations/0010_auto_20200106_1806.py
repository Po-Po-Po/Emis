# Generated by Django 3.0.1 on 2020-01-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files_manager', '0001_initial'),
        ('crm', '0009_auto_20200106_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='files',
            field=models.ManyToManyField(blank=True, null=True, related_name='equipment_files', to='files_manager.Attachment', verbose_name='Файлы'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='files',
            field=models.ManyToManyField(blank=True, null=True, related_name='personnel_files', to='files_manager.Attachment', verbose_name='Файлы'),
        ),
    ]