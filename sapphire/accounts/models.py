from django.db import models
from django.contrib.auth.models import User 


"""
Custom User class for this backend
"""
class Profile:
    timezone = models.CharField(max_length=50, default='EST')
    # A one to many relationship to team members that is connected when the
    # Profile is a TEAM_LEADER with people in their team.
    team = models.ForeignKey(
    'self',
    models.CASCADE
    )
    # The user variable to allow authentication to work
    user = models.OneToOneField(User)
