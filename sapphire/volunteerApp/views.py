from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timezone

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

def slot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    user_slots = User_Slot.objects.filter(parentSlot=slot)
    return render(request, 'volunteer/slot.html', {'slot':slot, 'user_slots':user_slots})

def slotNeeds(request):
    slots = Slot.objects.order_by('start')
    if request.user.is_authenticated():
        return render(request, 'volunteer/slots.html', {'slots':slots})
    else:
        return redirect('login')

def volunteer(request, slot_id):
    #next = request.GET.get('next')
    slot = Slot.objects.get(id=slot_id)
    user_slot = User_Slot.objects.filter(parentSlot=slot, volunteer__isnull=True).first()
    if (user_slot == None):
        return redirect('/volunteer/slot/'+str(slot_id))

    user_slot.volunteer = request.user
    user_slot.save()

    name = slot.title
    event = slot.parentEvent.name


    feed_entry = Feed_Entry(
        user=request.user,
        datetime=datetime.now(),
        description="Volunteered for \"" + name + "\" in event \"" + event + "\"",
        url="/volunteer/slot/" + str(slot.id))
    feed_entry.save()
    return redirect('/volunteer/slot/'+str(slot.id))


def signin(request, user_slot_id):
    user_slot = User_Slot.objects.get(id=user_slot_id)
    user_slot.signin = datetime.now(timezone.utc)
    user_slot.save()
    return redirect('/volunteer/slot/'+str(user_slot.parentSlot.id))


def signout(request, user_slot_id):
    user_slot = User_Slot.objects.get(id=user_slot_id)
    user_slot.signout = datetime.now(timezone.utc)
    deltaTime = user_slot.signout - user_slot.signin
    user_slot.difference = float(deltaTime.days * 86400) + float(deltaTime.seconds)
    user_slot.save()
    return redirect('/volunteer/slot/'+str(user_slot.parentSlot.id))
