from alerts.models import Alert

def getAlerts(request):
 alerts = getUserAlerts(request)
 return {'alerts': alerts}

def getUserAlerts(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    if (request.user.is_authenticated):
        return Alert.objects.filter(user=request.user, ip=ipaddress)#filter(user=user)
    else:
        return Alert.objects.filter(ip=ipaddress)
