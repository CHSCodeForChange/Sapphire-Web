from django.shortcuts import render

def addEvent(request):
    render(request, 'organizer/add_event.html')
def addSlot(request):
    render(request, 'organizer/add_slot.html')
def index(requst):
    redirect('/accounts/profiles')
