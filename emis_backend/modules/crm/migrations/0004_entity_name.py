# Generated by Django 3.0.1 on 2019-12-25 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20191226_0248'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='name',
            field=models.CharField(default='None', max_length=150, verbose_name='Наименование'),
            preserve_default=False,
        ),
    ]
