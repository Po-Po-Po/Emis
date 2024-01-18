# Generated by Django 3.1.6 on 2021-02-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0025_auto_20210227_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subdivision',
            name='personnel',
        ),
        migrations.AddField(
            model_name='subdivision',
            name='personnel',
            field=models.ManyToManyField(to='crm.Personnel', verbose_name='Сотрудник'),
        ),
    ]
