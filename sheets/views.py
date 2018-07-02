from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv

# google apis
# import gspread
# from googleapiclient import discovery
# from oauth2client.service_account import ServiceAccountCredentials


# models
from utility.models import Slot, User_Slot, Event
import datetime as dt


# Create your views here.


def fromslot(request, slot_id):
	slot = Slot.objects.get(id=slot_id)
	if request.user not in slot.parentGroup.organizers.all():
		return render(request, 'not_authorized.html')

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="slot_' + slot.title + '.csv"'

	writer = csv.writer(response)

	writer.writerow(["Sapphire", "CHS Code For Change"])
	writer.writerow([slot.parentEvent.parentGroup.name, slot.parentEvent.name, slot.title])
	writer.writerow([])
	writer.writerow(["First Name", "Last Name", "Time In", "Time Out", "Difference", "Payment"])

	user_slots = User_Slot.objects.filter(parentSlot=slot)

	for slot in user_slots:
		if (slot.volunteer == None):
			writer.writerow(["[No Volunteer]",
			                 "[No Volunteer]",
			                 excel_date(date1=slot.signin),
			                 excel_date(date1=slot.signout),
			                 slot.difference, slot.payment])
		else:
			writer.writerow([slot.volunteer.first_name,
			                 slot.volunteer.last_name,
			                 excel_date(date1=slot.signin),
			                 excel_date(date1=slot.signout),
			                 slot.difference, slot.payment])

	# scope = ['https://spreadsheets.google.com/feeds']
	# cred = ServiceAccountCredentials.from_json_keyfile_name('sapphire.json')
	# client = gspread.authorize(creds)
	# service = discovery.build('sheets', 'v4', credentials=cred)

	# body = {

	# }

	# sheet = service.spreadsheets().create(body=body)
	# sheet_request = None
	# response = sheet.execute()

	return response


def fromevent(request, event_id):
	event = Event.objects.get(id=event_id)
	slots = Slot.objects.filter(parentEvent=event)
	if request.user not in event.parentGroup.organizers.all():
		return render(request, 'not_authorized.html')

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="event_' + event.name + '.csv"'

	writer = csv.writer(response)

	writer.writerow(["Sapphire", "CHS Code For Change"])
	writer.writerow([event.parentGroup.name, event.name])

	for slot in slots:
		writer.writerow([])
		writer.writerow([slot.title])
		writer.writerow(["First Name", "Last Name", "Time In", "Time Out", "Difference", "Payment"])

		user_slots = User_Slot.objects.filter(parentSlot=slot)

		for user_slot in user_slots:
			if (user_slot.volunteer == None):
				writer.writerow(["[No Volunteer]",
				                 "[No Volunteer]",
				                 excel_date(date1=user_slot.signin),
				                 excel_date(date1=user_slot.signout),
				                 user_slot.difference, user_slot.payment])
			else:
				writer.writerow([user_slot.volunteer.first_name,
				                 user_slot.volunteer.last_name,
				                 excel_date(date1=user_slot.signin),
				                 excel_date(date1=user_slot.signout),
				                 user_slot.difference, user_slot.payment])

	return response


def excel_date(date1):
	if (date1 != None):
		return date1.strftime('%x %X')
	return None
