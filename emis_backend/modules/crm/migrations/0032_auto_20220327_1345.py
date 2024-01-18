# Generated by Django 3.1.7 on 2022-03-27 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files_manager', '0001_initial'),
        ('crm', '0031_auto_20220106_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.entity', verbose_name='Обьект'),
        ),
        migrations.AlterField(
            model_name='identity',
            name='_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files_manager.attachment', verbose_name='Загрузка удостоверения'),
        ),
        migrations.AlterField(
            model_name='identity',
            name='control',
            field=models.ManyToManyField(blank=True, null=True, to='crm.TypeControl', verbose_name='Вид контроля'),
        ),
    ]
