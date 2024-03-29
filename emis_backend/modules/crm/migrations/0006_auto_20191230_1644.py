# Generated by Django 3.0.1 on 2019-12-30 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files_manager', '__first__'),
        ('crm', '0005_auto_20191227_0439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entity',
            name='project',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='docs',
        ),
        migrations.AddField(
            model_name='entity',
            name='files',
            field=models.ManyToManyField(to='files_manager.Attachment', verbose_name='Файлы'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='files',
            field=models.ManyToManyField(to='files_manager.Attachment', verbose_name='Файлы'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='files',
            field=models.ManyToManyField(to='files_manager.Attachment', verbose_name='Файлы'),
        ),
    ]
