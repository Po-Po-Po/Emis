# Generated by Django 4.2.1 on 2023-05-14 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0042_delete_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='historytabel',
            name='work_day',
            field=models.IntegerField(default=0, max_length=10, verbose_name='Отработано дней'),
        ),
    ]