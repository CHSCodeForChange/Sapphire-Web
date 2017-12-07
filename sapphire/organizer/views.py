from django.shortcuts import render, redirect
from .forms import NewEventForm, NewSingleSlotForm
from utility.models import Event
from django.http import HttpResponse

# Sending user object to the form, to verify which fields to display/remove (depending on group)
def get_form_kwargs(self):
    kwargs = super(add, self).get_form_kwargs()
    kwargs.update({'user': self.request.user})
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
                slot = form.save(commit=False)
                slot.save()
        else:
            form = NewSingleSlotForm(user=request.user)
        # Filter this by single slot events in the future
        events = Event.objects.all()
        return render(request, 'organizer/add_single_slot.html', {'form':form, 'events':events})
    elif type == 'event':
        if(request.method == 'POST'):
            form = NewEventForm(request.POST, user=request.user)
            if form.is_valid():
                slot = form.save(commit=False)
                slot.save()
        else:
            form = NewEventForm(user=request.user)
        events = Event.objects.all()
        return render(request, 'organizer/add_event.html', {'form':form, 'events':events})

def index(request):
    return redirect('/accounts/profile')
def deleteEvent(request, event_id):
    next = request.GET.get('next')
    object = Event.objects.get(id=event_id)
    object.delete()
    return redirect(next)
