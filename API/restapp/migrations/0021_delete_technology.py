# Generated by Django 4.2 on 2023-07-17 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0020_rename_id_technology_auto_increment_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Technology',
        ),
    ]
