from django.shortcuts import render, redirect
from django.http import HttpResponse

from utility.models import *

def index(request):
    # Run processes to build dataset after login
    return redirect('feed')     # Redirects to /home/feed/
def feed(request):
    return render(request, "volunteer/feed.html")
    return HttpResponse("This is the volunteers feed as well as the default page while we get things started!")
def calendar(request):
    return render(request, "volunteer/calendar.html")
    return HttpResponse("This will be the calendar eventually.")
def eventNeeds(request):
    #return render(request, "volunteer/events.html")
    #return HttpResponse("This will be the Event Needs page where you can see a list of all the *events* that need volunteers to fill their slots.")
    events = Event.objects.all()
    return render(request, 'volunteer/events.html', {'events':events})
def event(request):
    event = Event.objects.all()
    return render(request, 'volunteer/event.html', {'event':event})
def slotNeeds(request):
    return HttpResponse("This will be the Slot Needs page where you can see a list of all the *slots* that need volunteers to fill for a specific event. This event is either chosen from a dropdown at the top or passed in when this page is loaded.")
