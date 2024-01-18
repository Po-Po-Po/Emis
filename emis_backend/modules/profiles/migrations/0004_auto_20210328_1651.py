# Generated by Django 3.1.6 on 2021-03-28 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0030_auto_20210328_1651'),
        ('profiles', '0003_customuser_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='history',
            field=models.ManyToManyField(blank=True, related_name='history_user', to='crm.History', verbose_name='История'),
        ),
    ]