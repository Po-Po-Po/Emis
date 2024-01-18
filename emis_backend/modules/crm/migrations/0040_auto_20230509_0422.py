# Generated by Django 3.1.7 on 2023-05-09 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0039_auto_20230509_0418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportcard',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='Заказчик'),
        ),
        migrations.AlterField(
            model_name='reportcard',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.personnel', verbose_name='Ответственный'),
        ),
    ]
