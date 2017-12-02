from django.db import models
from django.contrib.auth.models import User, UserManager
from accounts.models import Profile

"""
Notes:
I have used models.CASCADE in all the db relationship on_delete cases. I do not
know if this is good practice or will result in errors later down the line.
"""

"""
A slot object allows volunteers to sign up for it and has a start time and end
time. It has a parent Event.
"""
class Slot(models.Model):
    volunteers = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # TODO make sure this can only point to one Event and not more than that
    parentEvent = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    # The minimun number of volunteers this slot needs to have. Set by Event
    # organizer and factored into slot priority
    minVolunteers = models.IntegerField()
    # The maximum number of volunteers this slot can have. Set by Event
    # organizer and stops too many Profiles from signing up
    maxVolunteers = models.IntegerField()
    # TODO allow a getPriority() function to get the instantanious priority of
    # the Event object
class SingleSlot(models.Model):
    # The organizer of the Event
    organizer = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    # The string name of the Event
    name = models.CharField(max_length=80)
    # The String location of the Event
    location = models.CharField(max_length=240)
    # The list of Volunteers
    volunteers = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    # The minimun number of volunteers this slot needs to have. Set by Event
    # organizer and factored into slot priority
    minVolunteers = models.IntegerField()
    # The maximum number of volunteers this slot can have. Set by Event
    # organizer and stops too many Profiles from signing up
    maxVolunteers = models.IntegerField()
    # TODO allow a getPriority() function to get the instantanious priority of
    # the Event object
    in_person = models.BooleanField()



"""
This class is an object containing all the necessary information on an Event.
It contains instances of Slots and can be created by a Profile of type ORGANIZER
"""
class Event(models.Model):
    # The organizer of the Event
    organizer = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    # The string name of the Event
    name = models.CharField(max_length=80)
    # The String location of the Event
    location = models.CharField(max_length=240)
    # A one to many relationship holding the Slots for an Event object
    slots = models.ForeignKey(
        'Slot',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # TODO allow a getPriority() function to get the instantanious priority of
    # the Event object
