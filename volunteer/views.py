from django.shortcuts import render, redirect
from django.http import HttpResponse

from utility.models import *
from feed.models import Feed_Entry
from groups.models import Group
from alerts.models import Alert
from organizer.views import addUserSlot
from .forms import FilterTimeForm
from email.mime.image import MIMEImage
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from feed.models import Feed_Entry
from groups.models import Group
from alerts.models import Alert

from .helpers import get_dt


def index(request):
	return redirect('events')


def calendar(request):
	if request.user.is_authenticated():
		return render(request, "volunteer/calendar.html")
	else:
		return redirect('login')


def events(request):
	if request.user.is_authenticated():
		# events = Event.get_users_groups_events(request.user)

		# groups = Group.objects.filter(Q(volunteers=request.user) | Q(organizers=request.user))
		groups = Group.objects.filter(
			Q(owner=request.user) | Q(organizers=request.user) | Q(volunteers=request.user)).distinct()
		# Filters
		search = request.GET.get('q', '')
		groupfilter = request.GET.get('groupfilter', '')
		distancefilter = request.GET.get('distancefilter', '')
		daterangefilter = request.GET.get('daterangefilter', '')
		if distancefilter is not '':
			try:
				distance = int(distancefilter)
				# Do distance calculations here
			except ValueError:
				return redirect(
					'/volunteer/events?groupfilter=' + groupfilter + '&distancefilter=&daterangefilter=' + daterangefilter)
		# Filter events by interpreted GET attributes
		events = Event.objects.filter(parentGroup__in=groups)
		# Filter by group
		group_query = Q()
		for group in str.split(groupfilter, "_"):
			if not group == "":
				group_query |= Q(parentGroup=group)
		events = events.filter(group_query)
		# Filter by daterange
		if daterangefilter is not '':
			dates = str.split(daterangefilter, "_")
			if len(dates) == 2:
				try:
					start_date = datetime.strptime(dates[0], "%Y-%m-%d")
					end_date = datetime.strptime(dates[1], "%Y-%m-%d")
					events = events.filter(Q(start__gte=start_date) & Q(end__lte=end_date))
				except ValueError:
					pass
		# Filter by search query
		if search is not '':
			events = events.filter(Q(name__contains=search) | Q(location__contains=search) | Q(
				parentGroup__name__contains=search)).distinct()
		return render(request, 'volunteer/events.html',
								{'events': events, 'groups': groups, 'search': search, 'groupfilter': groupfilter,
								'distancefilter': distancefilter, 'daterangefilter': daterangefilter})
	else:
		return redirect('login')


def event(request, event_id):
	event = Event.objects.get(id=event_id)

	is_organizer = Group.get_is_organzer(event.parentGroup, request.user)
	volunteer = request.user

	slots = Slot.objects.order_by('start')
	return render(request, 'volunteer/event.html',
	              {'event': event, 'slots': slots, 'is_organizer': is_organizer, 'volunteer': volunteer})


def accept(request, slot_id):
	slot = Slot.objects.get(id=slot_id)
	us = User_Slot.objects.filter(parentSlot=slot, volunteer=request.user).first()
	if us is not None:
		us.accepted = "Yes"
		us.save()
	return redirect('/volunteer/slot/' + str(slot_id))


def slot(request, slot_id):
	slot = Slot.objects.get(id=slot_id)
	event = slot.parentEvent
	private = slot.private

	if (slot.parentEvent != None):
		is_organizer = Group.get_is_organzer(slot.parentEvent.parentGroup, request.user)
	else:
		is_organizer = Group.get_is_organzer(slot.parentGroup, request.user)

	user_slots = User_Slot.objects.filter(parentSlot=slot)
	is_volunteered = not (User_Slot.objects.filter(parentSlot=slot, volunteer=request.user).first() == None)
	pendingAccept = False
	if is_volunteered:
		pendingAccept = User_Slot.objects.filter(parentSlot=slot, volunteer=request.user).first().accepted == 'No'
		print(pendingAccept)

	volunteer = request.user
	specific_user_slot = User_Slot.objects.filter(parentSlot=slot, volunteer=request.user).first()

	if (len(User_Slot.objects.filter(parentSlot=slot)) != 0):
		percentFilled = int(len(User_Slot.objects.filter(parentSlot=slot).exclude(volunteer=None)) / len(
			User_Slot.objects.filter(parentSlot=slot)) * 100)
	else:
		percentFilled = 0
	for i in user_slots:
		i.prep_html()

	if pendingAccept:
		alert = Alert(user=request.user, text="You have been requested to volunteer for this slot", color=Alert.getBlue())
		alert.saveIP(request)

	return render(request, 'volunteer/slot.html',
	              {'slot': slot, 'user_slots': user_slots, 'event': event,
	               'full': User_Slot.objects.filter(parentSlot=slot, volunteer__isnull=True).first(),
	               'is_organizer': is_organizer,
	               'percentFilled': percentFilled, 'is_volunteered': is_volunteered, 'offer': pendingAccept,
	               'private': private, 'specific_user_slot': specific_user_slot,
	               'extra': (list(user_slots[0].get_extra().keys()) if (len(user_slots) > 0) else []),
	               'single': (slot.parentEvent == None)})


def slots(request):
	if request.user.is_authenticated():
		groups = Group.objects.filter(
			Q(owner=request.user) | Q(organizers=request.user) | Q(volunteers=request.user)).distinct()
		# Filters
		search = request.GET.get('q', '')
		groupfilter = request.GET.get('groupfilter', '')
		distancefilter = request.GET.get('distancefilter', '')
		daterangefilter = request.GET.get('daterangefilter', '')
		if distancefilter is not '':
			try:
				distance = int(distancefilter)
				# Do distance calculations here
			except ValueError:
				return redirect(
					'/volunteer/slots?groupfilter=' + groupfilter + '&distancefilter=&daterangefilter=' + daterangefilter)
		# Filter events by interpreted GET attributes
		slots = Slot.objects.filter(parentGroup__in=groups)
		# Filter by group
		group_query = Q()
		for group in str.split(groupfilter, "_"):
			if not group == "":
				group_query |= Q(parentGroup=group)
		slots = slots.filter(group_query)
		# Filter by daterange
		if daterangefilter is not '':
			dates = str.split(daterangefilter, "_")
			if len(dates) == 2:
				try:
					start_date = datetime.strptime(dates[0], "%Y-%m-%d")
					end_date = datetime.strptime(dates[1], "%Y-%m-%d")
					slots = slots.filter(Q(start__gte=start_date) & Q(end__lte=end_date))
				except ValueError:
					pass
		# Filter by search query
		if search is not '':
			slots = slots.filter(Q(title__contains=search) | Q(location__contains=search) | Q(
				parentGroup__name__contains=search)).distinct()
		return render(request, 'volunteer/slots.html',
								{'slots': slots, 'groups': groups, 'search': search, 'groupfilter': groupfilter,
								'distancefilter': distancefilter, 'daterangefilter': daterangefilter})
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

	if (slot.maxVolunteers == 0 and slots_filled_by_this_user == None):
		user_slot = User_Slot(parentSlot=slot, accepted="Yes")

	elif (slots_filled_by_this_user != None):
		alert = Alert(user=request.user, text="Already volunteered", color=Alert.getRed())
		alert.saveIP(request)
		return redirect('/volunteer/slot/' + str(slot_id))
	elif (user_slot == None):
		alert = Alert(user=request.user, text="Already at Max Volunteers", color=Alert.getRed())
		alert.saveIP(request)
		return redirect('/volunteer/slot/' + str(slot_id))

	user_slot.volunteer = request.user
	user_slot.accepted = "Yes"
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
		datetime=get_dt(),
		description="Volunteered for \"" + name,
		url="/volunteer/slot/" + str(slot.id),
		private=slot.private)
	feed_entry.save()

	alert = Alert(user=request.user, text="Volunteered for " + slot.title, color=Alert.getGreen())
	alert.saveIP(request)

	return redirect('/volunteer/slot/' + str(slot.id))


def volunteerForUser(request, slot_id, user_id):
	thisUser = User.objects.get(id=user_id)
	# next = request.GET.get('next')
	slot = Slot.objects.get(id=slot_id)
	group = slot.get_group()

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
		user_slot.accepted = "No"
		user_slot.save()

		name = slot.title
		event = slot.parentEvent

		feed_entry = Feed_Entry(
			group=group,
			user=thisUser,
			datetime=get_dt(),
			description="Accept volunteer for " + name,
			url="/volunteer/slot/" + str(slot.id),
			private=slot.private)
		feed_entry.save()

		alert = Alert(user=thisUser, text="Volunteered for " + slot.title, color=Alert.getGreen())
		alert.saveIP(request)

		current_site = get_current_site(request)

		# Sends the user an email based on the email template and the info passed in here
		message = render_to_string('emails/volentold.html', {
			'user': thisUser,
			'domain': current_site.domain,
			'slot': slot,
			'group':group,
		})

		mail_subject = 'You have been added to a slot'
		to_email = thisUser.email
		email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
		email.content_subtype = 'html'
		email.mixed_subtype = 'related'
		fp = open('static/img/logos.ico/ms-icon-70x70.png', 'rb')
		logo = MIMEImage(fp.read())
		logo.add_header('Content-ID', '<logo>')
		email.attach(logo)
		email.send()

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
		if (slot.maxVolunteers != 0):
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
		user_slot.signin = get_dt()
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
		user_slot.signout = get_dt()
		user_slot.save()
		user_slot.updateDeltaTimes()

		alert = Alert(user=request.user, text="Signed out " + user_slot.volunteer.username, color=Alert.getYellow())
		alert.saveIP(request)

	return redirect(next)
