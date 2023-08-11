# Generated by Django 4.2.1 on 2023-07-24 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0022_technology'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtsession',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='session', to='restapp.managedobject'),
        ),
        migrations.AlterField(
            model_name='managedobject',
            name='site_id',
            field=models.CharField(max_length=7, primary_key=True, serialize=False, unique=True),
        ),
    ]
