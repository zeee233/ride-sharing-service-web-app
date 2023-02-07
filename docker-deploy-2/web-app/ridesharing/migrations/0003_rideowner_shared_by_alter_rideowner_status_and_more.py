# Generated by Django 4.1.5 on 2023-02-02 00:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ridesharing', '0002_rideowner_status_alter_ride_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rideowner',
            name='shared_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ridesharing.ridesharer'),
        ),
        migrations.AlterField(
            model_name='rideowner',
            name='status',
            field=models.CharField(default='open', max_length=10),
        ),
        migrations.AlterField(
            model_name='ridesharer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
