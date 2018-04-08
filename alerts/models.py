from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


# Create your models here.

class Alert(models.Model):
    ip = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        null=True
    )

    text = models.CharField(max_length=120, default = "")
    color = models.CharField(max_length=20, default = "alert alert-success")
    url = models.URLField(blank=True)

    def getGreen():
        return "alert alert-success"

    def getBlue():
        return "alert alert-info"

    def getYellow():
        return "alert alert-warning"

    def getRed():
        return "alert alert-danger"

    def getUserAlerts(self, request):#, user):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        if (request.user.is_authenticated):
            return Alert.objects.filter(Q(user=request.user), Q(ip=ipaddress))#filter(user=user)
        else:
            return Alert.objects.filter(ip=ipaddress)

    def deleteAlert(self):
        self.delete()
        return False

    def saveIP(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        self.ip = ipaddress
        self.save()
