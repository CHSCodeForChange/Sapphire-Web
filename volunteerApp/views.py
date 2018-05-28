from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timezone, timedelta

from utility.models import *
from feed.models import Feed_Entry
from groups.models import Group
from alerts.models import Alert
from organizer.views import addUserSlot
from .forms import FilterTimeForm


def index(request):
    # Run processes to build dataset after login
    return redirect('eventNeeds')  # Redirects to /home/feed/


def calendar(request):
    if request.user.is_authenticated():
        return render(request, "volunteer/calendar.html")
    else:
        return redirect('login')


def eventNeeds(request):
    if request.user.is_authenticated():
        if (request.method == 'POST'):
            form = FilterTimeForm(request.POST)
            if form.is_valid():
                events = Event.get_users_groups_events(request.user).filter(
                    start__range=[form.getStart(), form.getEnd()])
        else:
            form = FilterTimeForm()
            events = Event.get_users_groups_events(request.user)

        return render(request, 'volunteer/events.html', {'events': events, 'form': form})
    else:
        return redirect('login')


def event(request, event_id):
    event = Event.objects.get(id=event_id)
    is_organizer = Group.get_is_organzer(event.parentGroup, request.user)

    slots = Slot.objects.order_by('start')
    return render(request, 'volunteer/event.html', {'event': event, 'slots': slots, 'is_organizer': is_organizer})


def slot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    event = slot.parentEvent
    if (slot.parentEvent != None):
        is_organizer = Group.get_is_organzer(slot.parentEvent.parentGroup, request.user)
    else:
        is_organizer = Group.get_is_organzer(slot.parentGroup, request.user)
    user_slots = User_Slot.objects.filter(parentSlot=slot)
    is_volunteered = not (User_Slot.objects.filter(parentSlot=slot, volunteer=request.user).first() == None)

    if (len(User_Slot.objects.filter(parentSlot=slot)) != 0):
        percentFilled = int(len(User_Slot.objects.filter(parentSlot=slot).exclude(volunteer=None)) / len(
            User_Slot.objects.filter(parentSlot=slot)) * 100)
    else:
        percentFilled = 0

    for i in user_slots:
        i.prep_html()
    if (slot.parentEvent != None):
        return render(request, 'volunteer/slot.html',
                  {'slot': slot, 'user_slots': user_slots, 'event': event, 'is_organizer': is_organizer,
                   'percentFilled': percentFilled, 'is_volunteered': is_volunteered,
                   'extra': (list(user_slots[0].get_extra().keys()) if (len(user_slots) > 0) else [])})
    else:
        return render(request, 'volunteer/singleSlot.html',
                  {'slot': slot, 'user_slots': user_slots, 'is_organizer': is_organizer,
                   'percentFilled': percentFilled, 'is_volunteered': is_volunteered,
                   'extra': (list(user_slots[0].get_extra().keys()) if (len(user_slots) > 0) else [])})


def slotNeeds(request):
    if request.user.is_authenticated():
        if (request.method == 'POST'):
            form = FilterTimeForm(request.POST)
            if form.is_valid():
                slots = Slot.get_users_groups_slots(request.user).filter(start__range=[form.getStart(), form.getEnd()])
        else:
            form = FilterTimeForm()
            slots = Slot.get_users_groups_slots(request.user)

        return render(request, 'volunteer/slots.html', {'slots': slots, 'form': form})
    else:
        return redirect('login')


def volunteer(request, slot_id):
    # next = request.GET.get('next')
    slot = Slot.objects.get(id=slot_id)
    user_slot = User_Slot.objects.filter(parentSlot=slot, volunteer__isnull=True).first()
    slots_filled_by_this_user = User_Slot.objects.filter(parentSlot=slot, volunteer=request.user).first()

    if (slot.parentEvent != None):
        group = slot.parentEvent.parentGroup
    else:
        group = slot.parentGroup

    if (user_slot == None or slots_filled_by_this_user != None):
        alert = Alert(user=request.user, text="Already volunteered", color=Alert.getRed())
        alert.saveIP(request)

        return redirect('/volunteer/slot/' + str(slot_id))

    user_slot.volunteer = request.user

    if (slot.get_extra() != None):
        ans = {}

        for i in slot.get_extra():
            if i != '':
                ans[i] = '-'
        user_slot.extraFields = ans
    user_slot.save()

    name = slot.title
    event = slot.parentEvent

    feed_entry = Feed_Entry(
        group=group,
        user=request.user,
        datetime=datetime.now(timezone.utc),
        description="Volunteered for \"" + name,
        url="/volunteer/slot/" + str(slot.id))
    feed_entry.save()

    alert = Alert(user=request.user, text="Volunteered for " + slot.title, color=Alert.getGreen())
    alert.saveIP(request)

    return redirect('/volunteer/slot/' + str(slot.id))


def volunteerForUser(request, slot_id, user_id):
    thisUser = User.objects.get(id=user_id)
    # next = request.GET.get('next')
    slot = Slot.objects.get(id=slot_id)

    if (slot.parentEvent != None):
        group = slot.parentEvent.parentGroup
    else:
        group = slot.parentGroup

    if group.get_is_organzer(request.user):
        user_slot = User_Slot.objects.filter(parentSlot=slot, volunteer__isnull=True).first()
        slots_filled_by_this_user = User_Slot.objects.filter(parentSlot=slot, volunteer=thisUser).first()
        if (slots_filled_by_this_user != None):
            alert = Alert(user=thisUser, text="Already volunteered", color=Alert.getRed())
            alert.saveIP(request)

            return redirect('/volunteer/slot/' + str(slot_id))
        if (user_slot == None):
            addUserSlot(request, slot_id)
            user_slot = User_Slot.objects.filter(parentSlot=slot, volunteer__isnull=True).first()

        user_slot.volunteer = thisUser
        user_slot.save()

        name = slot.title
        event = slot.parentEvent

        feed_entry = Feed_Entry(
            group=group,
            user=thisUser,
            datetime=datetime.now(timezone.utc),
            description="Volunteered for \"" + name,
            url="/volunteer/slot/" + str(slot.id))
        feed_entry.save()

        alert = Alert(user=thisUser, text="Volunteered for " + slot.title, color=Alert.getGreen())
        alert.saveIP(request)

    return redirect('/volunteer/slot/' + str(slot.id))


def unvolunteer(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    slots_filled_by_this_user = User_Slot.objects.filter(parentSlot=slot, volunteer=request.user).first()
    if (slots_filled_by_this_user == None):
        alert = Alert(user=request.user, text="Haven't volunteered yet", color=Alert.getRed())
        alert.saveIP(request)

        return redirect('/volunteer/slot/' + str(slot_id))
    else:
        slots_filled_by_this_user.delete()
        user_slot = User_Slot(parentSlot=slot, extraFields=slot.get_extra())
        user_slot.save()

        alert = Alert(user=request.user, text="unvolunteered for " + slot.title, color=Alert.getRed())
        alert.saveIP(request)

        return redirect('/volunteer/slot/' + str(slot_id))


def signin(request, user_slot_id):
    next = request.GET.get('next')

    user_slot = User_Slot.objects.get(id=user_slot_id)

    if (user_slot.parentSlot.parentEvent != None):
        group = user_slot.parentSlot.parentEvent.parentGroup
    else:
        group = user_slot.parentSlot.parentGroup

    if (user_slot.volunteer != None and group.get_is_organzer(request.user)):
        user_slot.signin = datetime.now(timezone.utc)
        user_slot.save()

        alert = Alert(user=request.user, text="Signed in " + user_slot.volunteer.username, color=Alert.getYellow())
        alert.saveIP(request)
    return redirect(next)


def signout(request, user_slot_id):
    next = request.GET.get('next')
    user_slot = User_Slot.objects.get(id=user_slot_id)

    if (user_slot.parentSlot.parentEvent != None):
        group = user_slot.parentSlot.parentEvent.parentGroup
    else:
        group = user_slot.parentSlot.parentGroup

    if (user_slot.volunteer != None and group.get_is_organzer(request.user)):
        user_slot.signout = datetime.now(timezone.utc)
        user_slot.save()
        user_slot.updateDeltaTimes()

        alert = Alert(user=request.user, text="Signed out " + user_slot.volunteer.username, color=Alert.getYellow())
        alert.saveIP(request)

    return redirect(next)
