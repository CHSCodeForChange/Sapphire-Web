from django.db import models
from django.contrib.auth.models import User, UserManager
from accounts.models import Profile
from groups.models import Group
from datetime import datetime, timedelta, timezone

"""
Notes:
I have used models.CASCADE in all the db relationship on_delete cases. I do not
know if this is good practice or will result in errors later down the line.
"""

"""
A slot object allows volunteers to sign up for it and has a start time and end
time. It has a parent Event.
"""

"""class Organization(models.Model):
    organizers = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # The list of Volunteers
    volunteers = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    events = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )"""



class Slot(models.Model):
    objects = models.Manager()
    # TODO make sure this can only point to one Event and not more than that
    parentEvent = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        null=False
    )
    start = models.DateTimeField()
    end = models.DateTimeField()

    # The minimun number of volunteers this slot needs to have. Set by Event
    # organizer and factored into slot priority
    minVolunteers = models.IntegerField()
    # The maximum number of volunteers this slot can have. Set by Event
    # organizer and stops too many Profiles from signing up
    maxVolunteers = models.IntegerField(null=True)
    # TODO allow a getPriority() function to get the instantanious priority of
    # the Event object

    title = models.CharField(max_length=240)
    # The String descriptionof the event
    description = models.CharField(max_length=960)

    # The String location Name of the Event
    location = models.CharField(max_length=240)
    # The String address of the Event
    address = models.CharField(max_length=240)
    # The String city of the Event'
    city = models.CharField(max_length=240)
    # The String state of event
    state = models.CharField(max_length=2)
    # The Integer zip code of the Event
    zip_code = models.IntegerField(null=True)


class User_Slot(models.Model):
    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    parentSlot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        null=False,
    )

    signin = models.DateTimeField(null=True)
    signout = models.DateTimeField(null=True)

    def is_signin_null(self):
        return self.signin == None

    def is_signout_null(self):
        return self.signout == None

    def is_volunteer_null(self):
      return self.volunteer == None

    difference = models.CharField(max_length=100, null=True)


class Event(models.Model):
    parentGroup = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=False,
    )
    #is_single = models.BooleanField(default=False)
    #type = models.CharField(max_length=80)
    objects = models.Manager()
    # The organizer of the Event
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )
    # The string name of the Event
    name = models.CharField(max_length=80)
    # The String descriptionof the event
    description = models.CharField(max_length=960)

    # The String location Name of the Event
    location = models.CharField(max_length=240)
    # The String address of the Event
    address = models.CharField(max_length=240)
    # The String city of the Event'
    city = models.CharField(max_length=240)
    # The String state of event
    state = models.CharField(max_length=2)
    # The Integer zip code of the Event
    zip_code = models.IntegerField(null=True)

    # The list of Volunteers
    """volunteers = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )"""

    slots = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="slot_set"
    )
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    # The minimun number of volunteers this slot needs to have. Set by Event
    # organizer and factored into slot priority
    #minVolunteers = models.IntegerField(null=True)
    # The maximum number of volunteers this slot can have. Set by Event
    # organizer and stops too many Profiles from signing up
    #maxVolunteers = models.IntegerField(null=True)
    # TODO allow a getPriority() function to get the instantanious priority of
    # the Event object
    #in_person = models.NullBooleanField(null=True)
    # A one to many relationship holding the Slots for an Event object


    # RAISING ERRORS


    # slots = models.ForeignKey(
    #     'Slot',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True
    # )
    def get_in_person(self):
        if self.in_person:
            return 'Yes'
        return 'No'



"""
|============|
| DEPRECATED |
|============|
This class is an object containing all the necessary information on an Event.
It contains instances of Slots and can be created by a Profile of type ORGANIZER

class Event(models.Model):
    objects = models.Manager()
    # The organizer of the Event
    organizer = models.ForeignKey(
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
"""
