from email.mime.image import MIMEImage
from itertools import chain

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.http import HttpResponse
import string

from django.template.loader import render_to_string

from .forms import NewEventForm, NewSingleSlotForm, NewSlotForm, UpdateEventForm, EditTimeForm, FieldForm, \
    UpdateSlotForm, SlotOpeningMailListForm
from utility.models import Event, Slot, User_Slot
from feed.models import Feed_Entry
from groups.models import Group
from alerts.models import Alert
from collections import OrderedDict

from .helpers import get_dt


# Sending user object to the form, to verify which fields to display/remove (depending on group)
def get_form_kwargs(self):
    kwargs = super(add, self).get_form_kwargs()
    kwargs.update({'user': User()})
    kwargs.update({'parentEvent': self.request.META.get('HTTP_REFERER')})
    kwargs.update({'volunteers': User()})
    kwargs.update({'organizers': User()})
    return kwargs


def console(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user not in event.parentGroup.organizers.all() and request.user != event.parentGroup.owner:
        return render(request, 'not_authorized.html')
    slots = Slot.objects.filter(parentEvent=event)
    print(slots)
    user_slots = None

    for slot in slots:
        if user_slots is None:
            user_slots = User_Slot.objects.filter(parentSlot=slot)
        else:
            slots_user_slots = User_Slot.objects.filter(parentSlot=slot)
            user_slots = user_slots | slots_user_slots

    return render(request, 'organizer/console.html', {'event': event, 'slots': slots, 'user_slots': user_slots})


def pick_group(request):
    my_groups = Group.get_is_organizer_list(request.user)
    return render(request, 'organizer/pick_group.html', {'groups': my_groups})


def pick_group_for_slot(request):
    my_groups = Group.get_is_organizer_list(request.user)
    return render(request, 'organizer/pick_group.html', {'groups': my_groups})


def addUserManually(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    if request.user not in slot.parentGroup.organizers.all() and request.user != slot.parentGroup.owner:
        return render(request, 'not_authorized.html')

    if slot.parentEvent is not None:
        group = slot.parentEvent.parentGroup
    else:
        group = slot.parentGroup

    if group.get_is_organzer(request.user):
        return render(request, 'organizer/pick_volunteer.html', {'slot': slot, 'group': group})

    return redirect('/volunteer/slot/' + str(slot.id))


def addEvent(request, group_id):
    group = Group.objects.get(id=group_id)
    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')

    if request.method == 'POST':
        form = NewEventForm(request.POST, user=request.user, parentGroup=group, initial={'private': group.private})
        if form.is_valid():
            event = form.save(commit=False)
            event.save()

            feed_entry = Feed_Entry(
                group=group,
                user=request.user,
                datetime=get_dt(),
                description="Created Event \"" + event.name + "\"",
                url="/volunteer/event/" + str(event.id),
                private=False)
            feed_entry.save()

            alert = Alert(user=request.user, text="Created event " + event.name, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect('/volunteer/events')
    else:
        form = NewEventForm(user=request.user, parentGroup=group, initial={'private': group.private})
    # Filter this by single slot events in the future
    return render(request, 'organizer/add_event.html', {'form': form})


def editEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    group = event.parentGroup
    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')
    if request.method == 'POST':
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
            event.private = data['private']

            event.save()

            alert = Alert(user=request.user, text="Updated Event " + event.name, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect('eventView', event_id)

    form = UpdateEventForm(id=event_id, initial={'title': event.name,
                                                 'description': event.description,
                                                 'location': event.location, 'address': event.address,
                                                 'city': event.city,
                                                 'state': event.state, 'zip_code': event.zip_code,
                                                 'start': event.start.strftime("%Y-%m-%dT%H:%M"),
                                                 'end': event.end.strftime("%Y-%m-%dT%H:%M"),
                                                 'private': event.private})

    return render(request, 'organizer/edit_event.html', {'form': form})


def addSlot(request, event_id):
    parentEvent = Event.objects.get(pk=event_id)
    group = parentEvent.parentGroup
    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')

    parentEvent = Event.objects.get(pk=event_id)

    if (request.method == 'GET'):
        form = NewSlotForm(user=request.user, parentEvent=parentEvent, initial={'private': parentEvent.private})
    else:
        # This line assumes the contents of the GET side of the if statement have already run (they should have) but its kinda janky
        form = NewSlotForm(request.POST, user=request.user, parentEvent=parentEvent,
                           initial={'private': parentEvent.private})
        if form.is_valid():
            slot = form.save(commit=False)
            slot.save()

            ans = OrderedDict()
            for i in slot.get_extra():
                if i != '' and i != ' ':
                    ans[i] = '-'
            print('ans for add is', ans)
            for x in range(0, slot.maxVolunteers):
                user_slot = User_Slot(volunteer=None, parentSlot=slot)
                user_slot.save_extra(ans)
                user_slot.save()

            feed_entry = Feed_Entry(
                group=group,
                user=request.user,
                datetime=get_dt(),
                description="Created slot \"" + str(slot.title) + "\" in event \"" + str(slot.parentEvent.name) + "\"",
                url="/volunteer/slot/" + str(slot.id),
                private=False)
            feed_entry.save()

            alert = Alert(user=request.user, text="Created slot " + slot.title, color=Alert.getBlue())
            alert.saveIP(request)

        return redirect('eventView', parentEvent.id)

    return render(request, 'organizer/add_slot.html', {'form': form})


def sendSlotOpeningNotification(request, slot_id):
    slot = Slot.objects.get(pk=slot_id)
    if request.user not in slot.parentGroup.organizers.all() and request.user != slot.parentGroup.owner:
        return render(request, 'not_authorized.html')
    group = slot.parentGroup
    if group is None:
        group = slot.parentEvent.parentGroup
    if request.method == 'POST':
        # form = SlotOpeningMailListForm(request.POST, all_members=list(chain(group.volunteers, group.organizers)))
        form = SlotOpeningMailListForm(request.POST, volunteers=group.volunteers, organizers=group.organizers)
        if form.is_valid():
            mail_list = form.cleaned_data.get('organizers').all() | form.cleaned_data.get('volunteers').all()
            current_site = get_current_site(request)
            for recipient in mail_list:
                message = render_to_string('emails/slot_create_alert.html', {
                    'user': recipient,
                    'slot': slot,
                    'group': group,
                    'domain': current_site.domain,
                })
                mail_subject = 'Sign up for a ' + group.name + ' Activity!'
                to_email = recipient.email
                email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
                email.content_subtype = 'html'
                email.mixed_subtype = 'related'
                fp = open('static/img/logos.ico/ms-icon-70x70.png', 'rb')
                logo = MIMEImage(fp.read())
                logo.add_header('Content-ID', '<logo>')
                email.attach(logo)
                email.send()
            return redirect('/volunteer/slot/' + str(slot_id))
    else:
        form = SlotOpeningMailListForm(volunteers=group.volunteers, organizers=group.organizers)

    return render(request, 'organizer/selectEmailRecipients.html', {'form': form})


def sendEventOpeningNotification(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user not in event.parentGroup.organizers.all() and request.user != event.parentGroup.owner:
        return render(request, 'not_authorized.html')
    group = event.parentGroup
    if request.method == 'POST':
        # form = SlotOpeningMailListForm(request.POST, all_members=list(chain(group.volunteers, group.organizers)))
        form = SlotOpeningMailListForm(request.POST, volunteers=group.volunteers, organizers=group.organizers)
        if form.is_valid():
            mail_list = form.cleaned_data.get('organizers').all() | form.cleaned_data.get('volunteers').all()
            current_site = get_current_site(request)
            for recipient in mail_list:
                message = render_to_string('emails/event_create_alert.html', {
                    'user': recipient,
                    'event': event,
                    'group': group,
                    'domain': current_site.domain,
                    'slots': Slot.objects.filter(parentEvent=event),
                })
                mail_subject = 'Sign up for a ' + group.name + ' Activity!'
                to_email = recipient.email
                email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
                email.content_subtype = 'html'
                email.mixed_subtype = 'related'
                fp = open('static/img/logos.ico/ms-icon-70x70.png', 'rb')
                logo = MIMEImage(fp.read())
                logo.add_header('Content-ID', '<logo>')
                email.attach(logo)
                email.send()
            return redirect('/volunteer/event/' + str(event_id))
    else:
        form = SlotOpeningMailListForm(volunteers=group.volunteers, organizers=group.organizers)

    return render(request, 'organizer/selectEmailRecipients.html', {'form': form})

def viewEventOpenningEmailPreview(request, event_id):
    event = Event.objects.get(id=event_id)
    group = event.parentGroup
    slots = event.slot_set.all()
    domain = get_current_site(request).domain

    return render(request, 'emails/event_create_alert.html', {'preview': True, 'event': event, 'group': group, 'slots': slots, 'domain': domain})


def addSingleSlot(request, group_id):
    group = Group.objects.get(id=group_id)
    if not Group.get_is_organzer(group, request.user):
        alert = Alert(user=request.user, text="Only organizers can add single slots", color=Alert.getRed())
        alert.saveIP(request)
        return redirect('/volunteer/slots')

    if request.method == 'GET':
        form = NewSlotForm(user=request.user, parentEvent=None, initial={'private': group.private})
    else:
        form = NewSlotForm(request.POST, user=request.user, parentEvent=None, initial={'private': group.private})
        if form.is_valid():
            slot = form.save(commit=False)
            slot.parentGroup = group
            slot.save()

            ans = OrderedDict()
            for i in slot.get_extra():
                if i != '' and i != ' ':
                    ans[i] = '-'
            for x in range(0, slot.maxVolunteers):
                user_slot = User_Slot(volunteer=None, parentSlot=slot)
                user_slot.save_extra(ans)
                user_slot.save()

            feed_entry = Feed_Entry(
                group=group,
                user=request.user,
                datetime=get_dt(),
                description="Created single slot \"" + str(slot.title),
                url="/volunteer/slot/" + str(slot.id),
                private=False)
            feed_entry.save()

            alert = Alert(user=request.user, text="Created slot " + slot.title, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect('/volunteer/slots/' + str(slot.id))

    return render(request, 'organizer/add_slot.html', {'form': form})


def editSlot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    parentEvent = slot.parentEvent
    group = slot.parentGroup
    if (group == None):
        group = slot.parentEvent.parentGroup
    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')
    if request.method == 'POST':
        form = UpdateSlotForm(request.POST, id=slot_id)
        if form.is_valid():
            data = form.save(commit=False)
            slot.start = data['start']
            slot.end = data['end']
            slot.title = data['title']
            slot.description = data['description']
            slot.location = data['location']
            slot.paymentPerHour = data['paymentPerHour']
            slot.extraFields = data['extraFields'].replace(' ', '')
            slot.private = data['private']

            unlimited = data['unlimited']
            if (unlimited):
                slot.maxVolunteers = 0
            else:
                slot.maxVolunteers = 1

            slot.save()

            newFields = slot.get_extra()
            for user in User_Slot.objects.filter(parentSlot=slot):
                ans = OrderedDict()
                for a in newFields:
                    if a != '':
                        val = ''
                        if a in list(user.get_extra().keys()):
                            val = user.get_extra()[a]

                        if val != '' and val != ' ':
                            ans[a] = val
                        else:
                            ans[a] = '-'
                        print(ans)
                user.save_extra(ans)
                user.save()

            feed_entry = Feed_Entry(
                group=group,
                user=request.user,
                datetime=get_dt(),
                description="Updated slot \"" + str(slot.title),
                url="/volunteer/slot/" + str(slot.id),
                private=False)
            feed_entry.save()

            alert = Alert(user=request.user, text="Updated Slot " + slot.title, color=Alert.getBlue())
            alert.saveIP(request)

            return redirect('/volunteer/slot/' + str(slot.id))

    form = UpdateSlotForm(id=slot_id, initial={'title': slot.title,
                                               'description': slot.description,
                                               'location': slot.location,
                                               'start': slot.start.strftime("%Y-%m-%dT%H:%M"),
                                               'end': slot.end.strftime("%Y-%m-%dT%H:%M"),
                                               'paymentPerHour': slot.paymentPerHour,
                                               'extraFields': slot.extraFields,
                                               'private': slot.private,
                                               'unlimited': (slot.maxVolunteers == 0)})

    return render(request, 'organizer/edit_slot.html', {'form': form})


def addUserSlot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    group = slot.parentGroup
    if group is None:
        group = slot.parentEvent.parentGroup
    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')
    if group.get_is_organzer(request.user):
        ans = OrderedDict()
        for i in slot.get_extra():
            if i != '' and i != ' ':
                ans[i] = '-'
        user_slot = User_Slot(parentSlot=slot)
        user_slot.save_extra(ans)
        user_slot.save()

        alert = Alert(user=request.user, text="Added a volunteer openning", color=Alert.getBlue())
        alert.saveIP(request)
    else:
        alert = Alert(user=request.user, text="Only organizers can add volunteer opennings", color=Alert.getRed())
        alert.saveIP(request)
    return redirect('/volunteer/slot/' + str(slot_id))


def removeUserSlot(request, user_slot_id):
    user_slot = User_Slot.objects.get(id=user_slot_id)
    slot = user_slot.parentSlot
    group = slot.parentGroup
    if group is None:
        group = slot.parentEvent.parentGroup
    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')
    if group.get_is_organzer(request.user) and len(User_Slot.objects.all()) > 1:
        user_slot.delete()

        alert = Alert(user=request.user, text="Deleted a volunteer openning", color=Alert.getRed())
        alert.saveIP(request)
    else:
        if not group.get_is_organzer(request.user):
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
    if user_slot.parentSlot.parentGroup is not None:
        group = user_slot.parentSlot.parentGroup
    else:
        group = user_slot.parentSlot.parentEvent.parentGroup
    if not Group.get_is_organzer(group, request.user):
        alert = Alert(user=request.user, text="You must be an organizer to edit extra fields",
                      color=Alert.getRed())
        alert.saveIP(request)
        return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))
    if group.get_is_organzer(request.user):
        if request.method == 'POST':
            form = FieldForm(request.POST)
            if form.is_valid():
                newVal = form.save()
                user_slot.set_extra(field, newVal)
                user_slot.save()
                return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))

        else:
            form = FieldForm(initial={"field": user_slot.get_extra()[field]})

        return render(request, 'organizer/editField.html',
                      {'form': form, 'user_slot': user_slot, 'slotField': field, 'val': user_slot.get_extra()[field]})

    return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))


def editSignIn(request, user_slot_id):
    user_slot = User_Slot.objects.get(id=user_slot_id)

    if user_slot.parentSlot.parentEvent is not None:
        group = user_slot.parentSlot.parentEvent.parentGroup
    else:
        group = user_slot.parentSlot.parentGroup

    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')
    if group.get_is_organzer(request.user):
        if request.method == 'POST':
            form = EditTimeForm(request.POST)
            if form.is_valid():
                sign_in = form.save()
                user_slot.signin = sign_in
                user_slot.save()
                user_slot.updateDeltaTimes()
                return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))

        else:
            form = EditTimeForm()

        return render(request, 'organizer/editTime.html', {'form': form, 'user_slot': user_slot, 'type': 'In'})

    return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))


def editSignOut(request, user_slot_id):
    user_slot = User_Slot.objects.get(id=user_slot_id)

    if user_slot.parentSlot.parentEvent is not None:
        group = user_slot.parentSlot.parentEvent.parentGroup
    else:
        group = user_slot.parentSlot.parentGroup

    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')
    if group.get_is_organzer(request.user):
        if request.method == 'POST':
            form = EditTimeForm(request.POST)
            if form.is_valid():
                signout = form.save()
                user_slot.signout = signout
                user_slot.save()
                user_slot.updateDeltaTimes()
                return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))

        else:
            form = EditTimeForm()

        return render(request, 'organizer/editTime.html', {'form': form, 'user_slot': user_slot, 'type': 'Out'})

    return redirect('/volunteer/slot/' + str(user_slot.parentSlot.id))


def edit(request):
    # Makes sure the user is an organizer
    is_organizer = False
    for g in request.user.groups.all():
        if g.name == 'Organizer':
            is_organizer = True
    if not is_organizer:
        return render(request, 'not_authorized.html')
    # Gets the page type
    type = request.GET.get('type', 'html')
    # If the page type is normal, send them to the single slot page for now
    if type == 'html' or type == 'singleSlot':
        if request.method == 'POST':
            form = NewSingleSlotForm(request.POST, user=request.user)
            if form.is_valid():
                slot = form.save(commit=False)
                slot.save()
        else:
            form = NewSingleSlotForm(user=request.user)
        # Filter this by single slot events in the future
        return render(request, 'organizer/add_single_slot.html', {'form': form})
    elif type == 'event':
        if request.method == 'POST':
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
    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')
    if group.get_is_organzer(request.user):
        name = object.name

        object.delete()

        feed_entry = Feed_Entry(
            group=group,
            user=request.user,
            datetime=get_dt(),
            description="Deleted event \"" + name + "\"",
            url="/volunteer/events",
            private=False
        )
        feed_entry.save()

        alert = Alert(user=request.user, text="Deleted event " + name, color=Alert.getRed())
        alert.saveIP(request)

        return redirect("/volunteer/events")

    else:
        alert = Alert(user=request.user, text="Only organizers can delete events", color=Alert.getRed())
        alert.saveIP(request)

        return redirect("/volunteer/event/" + str(object.id))


def deleteSlot(request, slot_id):
    slot = Slot.objects.get(id=slot_id)
    if slot.parentEvent is not None:
        group = slot.parentEvent.parentGroup
    else:
        group = slot.parentGroup

    if not Group.get_is_organzer(group, request.user):
        return render(request, 'not_authorized.html')
    if group.get_is_organzer(request.user):
        if slot.parentEvent is not None:
            name = slot.title
            event = slot.parentEvent
            slot.delete()

            feed_entry = Feed_Entry(
                group=event.parentGroup,
                user=request.user,
                datetime=get_dt(),
                description="Deleted slot \"" + name + "\" in event \"" + event.name + "\"",
                url="/volunteer/slots",
                private=False
            )

            feed_entry.save()

            alert = Alert(user=request.user, text="Deleted slot " + name, color=Alert.getRed())
            alert.saveIP(request)

            return redirect('/volunteer/event/' + str(event.id))
        else:
            name = slot.title
            group = slot.parentGroup
            slot.delete()

            feed_entry = Feed_Entry(
                group=slot.parentGroup,
                user=request.user,
                datetime=get_dt(),
                description="Deleted slot \"" + name + "\" in group \"" + group.name + "\"",
                url="/volunteer/slots",
                private=False
            )

            feed_entry.save()

            alert = Alert(user=request.user, text="Deleted slot " + name, color=Alert.getRed())
            alert.saveIP(request)

            return redirect('/groups/' + str(group.id))
    else:
        alert = Alert(user=request.user, text="Only organizers can delete slots", color=Alert.getRed())
        alert.saveIP(request)

        return redirect("/volunteer/slot/" + str(slot.id))