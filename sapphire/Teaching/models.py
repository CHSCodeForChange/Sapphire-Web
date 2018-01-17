from django.db import models

# Create your models here.
class Animal(models.Model):
    breed = models.CharField(max_length=80)
    color = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    legs = models.IntegerField(null=True)
    is_dog = models.NullBooleanField(null=True)
