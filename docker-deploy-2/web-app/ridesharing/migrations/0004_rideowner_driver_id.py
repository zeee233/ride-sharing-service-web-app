# Generated by Django 4.1.5 on 2023-02-02 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ridesharing', '0003_rideowner_shared_by_alter_rideowner_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rideowner',
            name='driver_id',
            field=models.IntegerField(default=0),
        ),
    ]
