# Generated by Django 4.2.1 on 2023-12-22 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0048_historytabel_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='historytabel',
            name='code',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Код ОКЗ'),
        ),
    ]
