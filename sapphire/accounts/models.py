from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom Profile linked to a User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    permission = {} #the key is the permission itself which can be a url or just a word for the permission the value is a list of orgainizations it can do this action for

    #add permission to the profile for the PERM and the ORG
    def addPermission(self, perm, org):
        if self.permission.get(perm,None) is None:
            self.permission[perm] = [org]
        else:
            self.permission[perm].extend(org)
    #checks to see if permission contains PERM for ORG
    def hasPerm(self, perm, org):
        for i in self.permission[perm]:
            if i == org:
                return True
        return False
    #checks to see if anyone has the permission adn returns authorized organizations
    def allWithPerm(self, perm):
        return self.permission.get(perm, None)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    #TODO: should be able to delete all the except: stuff after all the users have run this
    try:
        instance.profile.save()
    except:
        print("stuff")
        print(sender.username, sender.id)
        print(instance.username, instance.id)
        p = Profile.objects.filter(username = instance.get_username()).first()
        if p is None:
            print("cool")
            instance.profile = Profile(username=instance.get_username())
        else:
            print("cool a")
            instance.profile = p
        instance.profile.user = instance
        instance.save()