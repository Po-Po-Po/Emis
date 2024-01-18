# Generated by Django 3.0.1 on 2020-01-06 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files_manager', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0007_auto_20191230_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='files',
            field=models.ManyToManyField(blank=True, null=True, related_name='entity_files', to='files_manager.Attachment', verbose_name='Файлы'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь EMIS'),
        ),
    ]
