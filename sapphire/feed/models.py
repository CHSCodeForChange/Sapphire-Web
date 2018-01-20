from django.db import models
from django.contrib.auth.models import User, UserManager
from accounts.models import Profile

# Create your models here.
class Feed_Entry(models.Model):
    objects = models.Manager()

    # The user that did the action the feed entry is talking about
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    # The datetime that the user did said action
    datetime = models.DateTimeField()


    # The String description of the action
    description = models.CharField(max_length=960)
