from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from django.db.models import Q


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

    organizers = models.ManyToManyField(User, related_name="group_organizers")
    volunteers = models.ManyToManyField(User, related_name="group_volunteers")

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
    hours = models.IntegerField(default=0)

    #returns a list of groups that a given user is a part of at any level
    def get_is_member_list(user):
        return Group.objects.filter(Q(owner=user) | Q(organizers=user) | Q(volunteers=user))

    #returns a list of groups that a give user is a owner/organizer of
    def get_is_organizer_list(user):
        return Group.objects.filter(Q(owner=user) | Q(organizers=user))

    def get_is_member(self, user):
        groups = Group.get_is_member_list(user)
        for group in groups:
            if (group == self):
                return True
        return False

    def get_is_organzer(self, user):
        groups = Group.get_is_organizer_list(user)
        for group in groups:
            if (group == self):
                return True
        return False

    def get_role(self, user):
        if (self.owner == user):
            return "owner"

        for organizer in self.organizers:
            return "organizer"

        for volunteer in self.volunteers:
            return "volunteer"

        return "none"

class Chat_Entry(models.Model):
    objects = models.Manager()

    """The user that did the action the feed entry is talking about
        also if you click on the user it will redirect the page to the user's profile"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    parentGroup = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    # The datetime that the user did said action
    datetime = models.DateTimeField()

    # The String description of the action
    description = models.CharField(max_length=960)
