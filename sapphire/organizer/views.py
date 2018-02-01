from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import string

from .forms import NewEventForm, NewSingleSlotForm, NewSlotForm
from utility.models import Event, Slot, User_Slot
from feed.models import Feed_Entry


# Sending user object to the form, to verify which fields to display/remove (depending on group)
def get_form_kwargs(self):
    kwargs = super(add, self).get_form_kwargs()
    kwargs.update({'user': self.request.user})
    kwargs.update({'parentEvent': self.request.META.get('HTTP_REFERER')})
    return kwargs
def add(request):
    # Makes sure the user is an organizer
    is_organizer = False
    for g in request.user.groups.all():
        if g.name == 'Organizer':
            is_organizer = True
    if not is_organizer:
        return HttpResponse('You don\'t have the right permissions to see this page. You must be an Organizer to access this page.')
    # Gets the page type
    type = request.GET.get('type', 'html')
    # If the page type is normal, send them to the single slot page for now
    if type == 'html' or type == 'singleSlot':
        if(request.method == 'POST'):
            form = NewSingleSlotForm(request.POST, user=request.user)
            if form.is_valid():
                event = form.save(commit=False)
                event.save()

                feed_entry = Feed_Entry(
                    user=request.user,
                    datetime=datetime.now(),
                    description="Created single slot \"" + event.name + "\"",
                    url="/volunteer/event/" + str(event.id))
                feed_entry.save()

                return redirect('/volunteer/eventNeeds')
        else:
            form = NewSingleSlotForm(user=request.user)
        # Filter this by single slot events in the future
        return render(request, 'organizer/add_single_slot.html', {'form':form})
    elif type == 'event':
        if(request.method == 'POST'):
            form = NewEventForm(request.POST, user=request.user)
            if form.is_valid():
                event = form.save(commit=False)
                event.save()

                feed_entry = feed_entry = Feed_Entry(
                    user=request.user,
                    datetime=datetime.now(),
                    description="Created event \"" + event.name + "\"",
                    url="/volunteer/event/" + str(event.id))
                feed_entry.save()

                return redirect('/volunteer/eventNeeds')
        else:
            form = NewEventForm(user=request.user)
        return render(request, 'organizer/add_event.html', {'form':form})

def addSlot(request, event_id):
    is_organizer = False
    for g in request.user.groups.all():
        if g.name == 'Organizer':
            is_organizer = True
    if not is_organizer:
        return HttpResponse('You don\'t have the right permissions to see this page. You must be an Organizer to access this page.')

    parentEvent = Event.objects.get(pk=event_id)

    if(request.method == 'GET'):
        form = NewSlotForm(user=request.user, parentEvent=parentEvent)
    else:
        #This line assumes the contents of the GET side of the if statement have already run (they should have) but its kinda janky
        form = NewSlotForm(request.POST, user=request.user, parentEvent=parentEvent)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.save()

            for x in range(0,slot.maxVolunteers):
                user_slot = User_Slot(volunteer=None, parentSlot=slot)
                user_slot.save()

            feed_entry = Feed_Entry(
                user=request.user,
                datetime=datetime.now(),
                description="Created slot \"" + str(slot.title) + "\" in event \"" + str(slot.parentEvent) + "\"",
                url="/volunteer/slot/" + str(slot.id))
            feed_entry.save()


            return redirect('eventView', parentEvent.id)

    return render(request, 'organizer/add_slot.html', {'form':form})


def edit(request):
    # Makes sure the user is an organizer
    is_organizer = False
    for g in request.user.groups.all():
        if g.name == 'Organizer':
            is_organizer = True
    if not is_organizer:
        return HttpResponse('You don\'t have the right permissions to see this page. You must be an Organizer to access this page.')
    # Gets the page type
    type = request.GET.get('type', 'html')
    # If the page type is normal, send them to the single slot page for now
    if type == 'html' or type == 'singleSlot':
        if(request.method == 'POST'):
            form = NewSingleSlotForm(request.POST, user=request.user)
            if form.is_valid():
                slot = form.save(commit=False)
                slot.save()
        else:
            form = NewSingleSlotForm(user=request.user)
        # Filter this by single slot events in the future
        return render(request, 'organizer/add_single_slot.html', {'form':form})
    elif type == 'event':
        if(request.method == 'POST'):
            form = NewEventForm(request.POST, user=request.user)
            if form.is_valid():
                slot = form.save(commit=False)
                slot.save()
        else:
            form = NewEventForm(user=request.user)
        return render(request, 'organizer/add_event.html', {'form':form})

def index(request):
    return redirect('/accounts/profile')

def deleteEvent(request, event_id):
    next = request.GET.get('next')
    object = Event.objects.get(id=event_id)
    name = object.name

    object.delete()

    feed_entry = Feed_Entry(
        user=request.user,
        datetime=datetime.now(),
        description="Deleted event \"" + name + "\"",
        url="/volunteer/eventNeeds"
    )
    feed_entry.save()

    return redirect("/volunteer/eventNeeds")

def deleteSlot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    name = slot.title
    event = slot.parentEvent
    slot.delete()

    feed_entry = Feed_Entry(
        user=request.user,
        datetime=datetime.now(),
        description="Deleted slot \"" + name + "\" in event \"" + event.name + "\"",
        url="/volunteer/slots"
    )
    feed_entry.save()
    return redirect('/volunteer/event/'+str(event.id))
