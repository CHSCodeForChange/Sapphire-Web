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
def slotNeeds(request):
    return HttpResponse("This will be the Slot Needs page where you can see a list of all the *slots* that need volunteers to fill for a specific event. This event is either chosen from a dropdown at the top or passed in when this page is loaded.")
