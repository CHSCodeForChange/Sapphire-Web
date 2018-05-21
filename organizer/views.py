from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timezone
import string

from .forms import NewEventForm, NewSingleSlotForm, NewSlotForm, UpdateEventForm, EditTimeForm, FieldForm, \
    UpdateSlotForm
from utility.models import Event, Slot, User_Slot
from feed.models import Feed_Entry
from groups.models import Group
from alerts.models import Alert


# Sending user object to the form, to verify which fields to display/remove (depending on group)
def get_form_kwargs(self):
    kwargs = super(add, self).get_form_kwargs()
    kwargs.update({'user': self.request.user})
    kwargs.update({'parentEvent': self.request.META.get('HTTP_REFERER')})
    return kwargs


def pick_group(request):
    my_groups = Group.get_is_organizer_list(request.user)
    return render(request, 'organizer/pick_group.html', {'groups': my_groups})


def addUserManually(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    group = slot.parentEvent.parentGroup
    if (group.get_is_organzer(request.user)):
        return render(request, 'organizer/pick_volunteer.html', {'slot': slot, 'group': group})
    return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))


def addEvent(request, group_id):
    group = Group.objects.get(id=group_id)
    if not Group.get_is_organzer(group, request.user):
        return HttpResponse(
            'You don\'t have the right permissions to see this page. You must be an Organizer to access this page.')

    if (request.method == 'POST'):
        form = NewEventForm(request.POST, user=request.user, parentGroup=group)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()

            feed_entry = Feed_Entry(
                group=group,
                user=request.user,
                datetime=datetime.now(timezone.utc),
                description="Created single slot \"" + event.name + "\"",
                url="/volunteer/event/" + str(event.id))
            feed_entry.save()

            alert = Alert(user=request.user, text="Created event " + event.name, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect('/volunteer/eventNeeds')
    else:
        form = NewEventForm(user=request.user, parentGroup=group)
    # Filter this by single slot events in the future
    return render(request, 'organizer/add_event.html', {'form': form})


def editEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user.is_authenticated():
        form = UpdateEventForm(request.POST, id=event_id)
        if form.is_valid():
            data = form.save(commit=False)
            event.name = data['title']
            event.description = data['description']
            event.location = data['location']
            event.address = data['address']
            event.city = data['city']
            event.state = data['state']
            event.zip_code = data['zip_code']
            event.start = data['start']
            event.end = data['end']

            event.save()

            alert = Alert(user=request.user, text="Updated Event " + event.name, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect('eventView', event_id)

    form = UpdateEventForm(id=event_id, initial={'title': event.name,
                                                 'description': event.description,
                                                 'location': event.location, 'address': event.address,
                                                 'city': event.city,
                                                 'state': event.state, 'zip_code': event.zip_code, 'start': event.start,
                                                 'end': event.end})

    return render(request, 'organizer/edit_event.html', {'form': form})


def addSlot(request, event_id):
    parentEvent = Event.objects.get(pk=event_id)
    group = parentEvent.parentGroup
    if not Group.get_is_organzer(group, request.user):
        return HttpResponse(
            'You don\'t have the right permissions to see this page. You must be an Organizer to access this page.')

    parentEvent = Event.objects.get(pk=event_id)

    if (request.method == 'GET'):
        form = NewSlotForm(user=request.user, parentEvent=parentEvent)
    else:
        # This line assumes the contents of the GET side of the if statement have already run (they should have) but its kinda janky
        form = NewSlotForm(request.POST, user=request.user, parentEvent=parentEvent)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.save()

            ans = {}
            for i in slot.get_extra():
                if i != '':
                    ans[i] = '-'
            for x in range(0, slot.maxVolunteers):
                user_slot = User_Slot(volunteer=None, parentSlot=slot, extraFields=ans)
                user_slot.save()

            feed_entry = Feed_Entry(
                group=group,
                user=request.user,
                datetime=datetime.now(timezone.utc),
                description="Created slot \"" + str(slot.title) + "\" in event \"" + str(slot.parentEvent) + "\"",
                url="/volunteer/slot/" + str(slot.id))
            feed_entry.save()

            alert = Alert(user=request.user, text="Created slot " + slot.title, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect('eventView', parentEvent.id)

    return render(request, 'organizer/add_slot.html', {'form': form})


def editSlot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    parentEvent = slot.parentEvent
    group = parentEvent.parentGroup

    if request.user.is_authenticated():
        form = UpdateSlotForm(request.POST, id=slot_id)
        if form.is_valid():
            data = form.save(commit=False)
            slot.start = data['start']
            slot.end = data['end']
            slot.title = data['title']
            slot.description = data['description']
            slot.location = data['location']
            slot.paymentPerHour = data['paymentPerHour']

            slot.save()

            feed_entry = Feed_Entry(
                group=group,
                user=request.user,
                datetime=datetime.now(timezone.utc),
                description="Updated slot \"" + str(slot.title) + "\" in event \"" + str(slot.parentEvent) + "\"",
                url="/volunteer/slot/" + str(slot.id))
            feed_entry.save()

            alert = Alert(user=request.user, text="Updated Slot " + slot.title, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect('slotView', slot.id)

    form = UpdateSlotForm(id=slot_id, initial={'title': slot.title,
                                               'description': slot.description,
                                               'location': slot.location, 'start': slot.start, 'end': slot.end,
                                               'paymentPerHour': slot.paymentPerHour})

    return render(request, 'organizer/edit_slot.html', {'form': form})


def addUserSlot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    group = slot.parentEvent.parentGroup
    if (group.get_is_organzer(request.user)):
        user_slot = User_Slot(parentSlot=slot, extraFields=slot.extraFields)
        user_slot.save()

        alert = Alert(user=request.user, text="Added a volunteer openning", color=Alert.getBlue())
        alert.saveIP(request)
    else:
        alert = Alert(user=request.user, text="Only organizers can add volunteer opennings", color=Alert.getRed())
        alert.saveIP(request)
    return redirect('/volunteer/slot/' + str(slot_id))


def removeUserSlot(request, user_slot_id):
    user_slot = User_Slot.objects.get(id=user_slot_id)
    group = user_slot.parentSlot.parentEvent.parentGroup
    if (group.get_is_organzer(request.user) and len(User_Slot.objects.all()) > 1):
        user_slot.delete()

        alert = Alert(user=request.user, text="Deleted a volunteer openning", color=Alert.getRed())
        alert.saveIP(request)
    else:
        if (group.get_is_organzer(request.user) == False):
            alert = Alert(user=request.user, text="Only organizers can delete volunteer opennings",
                          color=Alert.getRed())
            alert.saveIP(request)
        else:
            alert = Alert(user=request.user, text="A slot must have at lease 1 volunteer openning!",
                          color=Alert.getRed())
            alert.saveIP(request)

    return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))


def editField(request, user_slot_id, field):
    user_slot = User_Slot.objects.get(id=user_slot_id)
    group = user_slot.parentSlot.parentEvent.parentGroup
    if (group.get_is_organzer(request.user)):
        if (request.method == 'POST'):
            form = FieldForm(request.POST)
            if form.is_valid():
                newVal = form.save()
                user_slot.set_extra(field, newVal)
                user_slot.save()
                return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))

        else:
            form = FieldForm()

        return render(request, 'organizer/editSignIn.html', {'form': form, 'user_slot': user_slot})

    return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))


def editSignIn(request, user_slot_id):
    user_slot = User_Slot.objects.get(id=user_slot_id)
    group = user_slot.parentSlot.parentEvent.parentGroup
    if (group.get_is_organzer(request.user)):
        if (request.method == 'POST'):
            form = EditTimeForm(request.POST)
            if form.is_valid():
                sign_in = form.save()
                user_slot.signin = sign_in
                user_slot.save()
                user_slot.updateDeltaTimes()
                return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))

        else:
            form = EditTimeForm()

        return render(request, 'organizer/editSignIn.html', {'form': form, 'user_slot': user_slot})

    return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))


def editSignOut(request, user_slot_id):
    user_slot = User_Slot.objects.get(id=user_slot_id)
    group = user_slot.parentSlot.parentEvent.parentGroup
    if (group.get_is_organzer(request.user)):
        if (request.method == 'POST'):
            form = EditTimeForm(request.POST)
            if form.is_valid():
                signout = form.save()
                user_slot.signout = signout
                user_slot.save()
                user_slot.updateDeltaTimes()
                return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))

        else:
            form = EditTimeForm()

        return render(request, 'organizer/editSignOut.html', {'form': form, 'user_slot': user_slot})

    return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))


def edit(request):
    # Makes sure the user is an organizer
    is_organizer = False
    for g in request.user.groups.all():
        if g.name == 'Organizer':
            is_organizer = True
    if not is_organizer:
        return HttpResponse(
            'You don\'t have the right permissions to see this page. You must be an Organizer to access this page.')
    # Gets the page type
    type = request.GET.get('type', 'html')
    # If the page type is normal, send them to the single slot page for now
    if type == 'html' or type == 'singleSlot':
        if (request.method == 'POST'):
            form = NewSingleSlotForm(request.POST, user=request.user)
            if form.is_valid():
                slot = form.save(commit=False)
                slot.save()
        else:
            form = NewSingleSlotForm(user=request.user)
        # Filter this by single slot events in the future
        return render(request, 'organizer/add_single_slot.html', {'form': form})
    elif type == 'event':
        if (request.method == 'POST'):
            form = NewEventForm(request.POST, user=request.user)
            if form.is_valid():
                slot = form.save(commit=False)
                slot.save()
        else:
            form = NewEventForm(user=request.user)
        return render(request, 'organizer/add_event.html', {'form': form})


def index(request):
    return redirect('/accounts/profile')


def deleteEvent(request, event_id):
    object = Event.objects.get(id=event_id)
    group = object.parentGroup
    if (group.get_is_organzer(request.user)):
        name = object.name

        object.delete()

        feed_entry = Feed_Entry(
            group=group,
            user=request.user,
            datetime=datetime.now(timezone.utc),
            description="Deleted event \"" + name + "\"",
            url="/volunteer/eventNeeds"
        )
        feed_entry.save()

        alert = Alert(user=request.user, text="Deleted event " + name, color=Alert.getRed())
        alert.saveIP(request)

        return redirect("/volunteer/eventNeeds")

    else:
        alert = Alert(user=request.user, text="Only organizers can delete events", color=Alert.getRed())
        alert.saveIP(request)

        return redirect("/volunteer/event/" + str(object.id))


def deleteSlot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    group = slot.parentEvent.parentGroup
    if (group.get_is_organzer(request.user)):
        name = slot.title
        event = slot.parentEvent
        slot.delete()

        feed_entry = Feed_Entry(
            group=event.parentGroup,
            user=request.user,
            datetime=datetime.now(timezone.utc),
            description="Deleted slot \"" + name + "\" in event \"" + event.name + "\"",
            url="/volunteer/slots"
        )

        feed_entry.save()

        alert = Alert(user=request.user, text="Deleted slot " + name, color=Alert.getRed())
        alert.saveIP(request)

        return redirect('/volunteer/event/' + str(event.id))
    else:
        alert = Alert(user=request.user, text="Only organizers can delete slots", color=Alert.getRed())
        alert.saveIP(request)

        return redirect("/volunteer/slot/" + str(slot.id))
