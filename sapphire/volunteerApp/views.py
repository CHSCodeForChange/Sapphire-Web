from django.shortcuts import render, redirect
from django.http import HttpResponse

from utility.models import *

def index(request):
    # Run processes to build dataset after login
    return redirect('feed')     # Redirects to /home/feed/
def feed(request):
    if request.user.is_authenticated():
        return render(request, "volunteer/feed.html")
    else:
        return redirect('login')

def calendar(request):
    if request.user.is_authenticated():
        return render(request, "volunteer/calendar.html")
    else:
        return redirect('login')

def eventNeeds(request):
    events = Event.objects.all()
    if request.user.is_authenticated():
        return render(request, 'volunteer/events.html', {'events':events})
    else:
        return redirect('login')

def event(request):
    events = Event.objects.all()
    return render(request, 'volunteer/event.html', {'events':events})

def slot(request):
    slot = Slot.objects.all()
    return render(request, 'volunteer/slot.html', {'slot':slot})

def slotNeeds(request):
    slots = Slot.objects.all()
    if request.user.is_authenticated():
        return render(request, 'volunteer/slots.html', {'slots':slots})
    else:
        return redirect('login')
