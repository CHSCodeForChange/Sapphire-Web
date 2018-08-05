from django.db import models

from django.contrib.auth.models import User
from accounts.models import Profile
from groups.models import Group


class Feed_Entry(models.Model):
    def __str__(self):
        return 'Feed_Entry: ' + self.description[:500]
    objects = models.Manager()

    """The user that did the action the feed entry is talking about
        also if you click on the user it will redirect the page to the user's profile"""
    user = models.ForeignKey(
        User,
        related_name='notifs',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    # The datetime that the user did said action
    datetime = models.DateTimeField(blank=True, )

    # The String description of the action
    description = models.CharField(blank=True, max_length=960)

    # the URL that the feed redirects to if you click the description
    url = models.CharField(blank=True, max_length=120)

    private = models.BooleanField(blank=False, null=False, default=False)


    def get_navbar_notifs(notifs):
        return notifs.order_by('-datetime')[:5]