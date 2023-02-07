from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class RideOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=50)
    arrival_date_time = models.DateTimeField()
    number_passengers = models.PositiveSmallIntegerField()
    #CharField is used to store small amounts of text
    vehicle_type = models.CharField(max_length=20, blank=True, null=True)
    #TextField is used to store larger amounts of text
    special_requests = models.TextField(blank=True, null=True)
    is_shared = models.BooleanField(default=False)
    status = models.CharField(default='open', max_length=10)
    driver_id = models.IntegerField(unique=False, null=True)
    number_requested = models.PositiveSmallIntegerField()


class RideSharer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=50)
    earliest_arrival = models.DateTimeField()
    latest_arrival = models.DateTimeField()
    number_passengers = models.PositiveSmallIntegerField()
    ride_owner = models.ForeignKey(RideOwner, on_delete=models.CASCADE, related_name='ridesharers')
    

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    license_plate_number = models.CharField(max_length=20)
    max_passengers = models.PositiveSmallIntegerField()
    special_vehicle_info = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name+' '+self.vehicle_type+' '+str(self.max_passengers)
        
class Ride(models.Model):
    # one owner can have multiple rides while one ride can only have one owner
    owner = models.ForeignKey(RideOwner, on_delete=models.CASCADE)
    sharers = models.ManyToManyField(RideSharer)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    #if completed, the status will change to the closed
    status = models.CharField(max_length=10, default='open')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
