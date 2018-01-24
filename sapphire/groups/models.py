from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from utility.models import Slot, Event

class Group(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=120)


    # A super short description of the group
    tagline = models.CharField(max_length=120)
    # The String descriptionof the event
    description = models.CharField(max_length=960)

    email = models.EmailField(null=True)

    website = models.URLField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="group_owner"
    )

    organizers = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="group_organizers"
    )
    volunteers = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="group_volunteers"
    )

    events = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="group_event_set"
    )

    slots = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="group_slot_set"
    )

    # TODO make sure this can only point to one Event and not more than that


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

    #number of hours of service completed by this group
    hours = models.IntegerField(null=True)
