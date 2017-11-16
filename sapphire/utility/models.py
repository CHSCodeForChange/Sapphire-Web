from django.db import models
from django.contrib.auth.models import User, UserManager

"""
Notes:
I have used models.CASCADE in all the db relationship on_delete cases. I do not
know if this is good practice or will result in errors later down the line.
"""



"""
Custom User class for this backend
"""
class Profile(User):
    timezone = models.charField(max_length=50, default='EST')
    # A one to many relationship to team members that is connected when the
    # Profile is a TEAM_LEADER with people in their team.
    team = models.ForeignKey(
    Profile,
    models.CASCADE
    )

    objects = UserManager()

"""
This class is an object containing all the necessary information on an Event.
It contains instances of Slots and can be created by a Profile of type ORGANIZER
"""
class Event(models.Model):
    # The organizer of the Event
    organizer = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    # The string name of the Event
    name = models.CharField(max_length=80)
    # The String location of the Event
    location = models.CharField(max_length=240)
    # A one to many relationship holding the Slots for an Event object
    slots = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE
    )
    # TODO allow a getPriority() function to get the instantanious priority of
    # the Event object

"""
A slot object allows volunteers to sign up for it and has a start time and end
time. It has a parent Event.
"""
class Slot(models.Model):
    volunteers = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    # TODO make sure this can only point to one Event and not more than that
    event = ForeignKey(
        Event,
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
