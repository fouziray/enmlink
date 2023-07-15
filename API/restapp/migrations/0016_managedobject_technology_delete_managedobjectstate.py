# Generated by Django 4.2 on 2023-07-15 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0015_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagedObject',
            fields=[
                ('site_id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('wilaya', models.CharField(max_length=100, null=True)),
                ('UOP', models.CharField(choices=[('EAST', 'EAST'), ('CENTER', 'CENTER'), ('SOUTH', 'SOUTH')], max_length=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('3G', '3G'), ('4G', '4G'), ('2G', '2G')], max_length=2)),
                ('state', models.JSONField(verbose_name='state')),
                ('managedObject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='managedObject', to='restapp.managedobject')),
            ],
        ),
        migrations.DeleteModel(
            name='ManagedObjectState',
        ),
    ]
