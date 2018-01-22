from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime

from utility.models import *
from feed.models import Feed_Entry

def index(request):
    # Run processes to build dataset after login
    return redirect('eventNeeds')     # Redirects to /home/feed/


def calendar(request):
    if request.user.is_authenticated():
        return render(request, "volunteer/calendar.html")
    else:
        return redirect('login')

def eventNeeds(request):
    events = Event.objects.order_by('start')
    if request.user.is_authenticated():
        return render(request, 'volunteer/events.html', {'events':events})
    else:
        return redirect('login')

def event(request):
    is_organizer = False
    for g in request.user.groups.all():
        if g.name == 'Organizer':
            is_organizer = True

    print ("hi")

    events = Event.objects.all()
    slots = Slot.objects.order_by('start')
    return render(request, 'volunteer/event.html', {'events':events, 'slots':slots, 'is_organizer':is_organizer})

def slot(request):
    slot = Slot.objects.all()
    return render(request, 'volunteer/slot.html', {'slot':slot})

def slotNeeds(request):
    slots = Slot.objects.order_by('start')
    if request.user.is_authenticated():
        return render(request, 'volunteer/slots.html', {'slots':slots})
    else:
        return redirect('login')

def volunteer(request, slot_id):
    #next = request.GET.get('next')
    slot = Slot.objects.get(id=slot_id)
    name = slot.title
    event = slot.parentEvent.name
    slot.volunteers = request.user
    slot.save()

    feed_entry = Feed_Entry(
        user=request.user,
        datetime=datetime.now(),
        description="Volunteered for \"" + name + "\" in event \"" + event + "\"",
        url="/volunteer/slot/" + str(slot.id))
    feed_entry.save()
    return redirect('eventNeeds')
