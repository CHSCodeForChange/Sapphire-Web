from django.db import models

# Create your models here.
class Event (models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    location_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()

class Slot (models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()

class SingleSlot (models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    location_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
