# Generated by Django 3.0.1 on 2020-02-18 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_entity_director_lnr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entity',
            old_name='director_lnr',
            new_name='director_lnk',
        ),
    ]
