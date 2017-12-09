from django.db import models
from django.contrib.auth.models import User


# Custom Profile linked to a User
class Profile(models.Model):
    # The manager to get Profile objects
    objects = models.Manager()
    # The primary key
    # uid = models.IntegerField(primary_key=True)
    timezone = models.CharField(max_length=50, default='EST')
    # A one to many relationship to team members that is connected when the
    # Profile is a TEAM_LEADER with people in their team.
    team = models.ForeignKey(
        'self',
        models.CASCADE,
        null=True
    )
    # The user variable to allow authentication to work
    username = models.CharField(max_length=200, default = "")
    bio = models.CharField(max_length=1000, default = "")
    hours = models.IntegerField(default=0)
