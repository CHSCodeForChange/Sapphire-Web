from django.db import models

from django.contrib.auth.models import User, UserManager
from accounts.models import Profile
from groups.models import Group

# Create your models here.
class Feed_Entry(models.Model):
    objects = models.Manager()

    """The user that did the action the feed entry is talking about
        also if you click on the user it will redirect the page to the user's profile"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    # The datetime that the user did said action
    datetime = models.DateTimeField()

    # The String description of the action
    description = models.CharField(max_length=960)

    #the URL that the feed redirects to if you click the description
    url = models.CharField(max_length=120)
