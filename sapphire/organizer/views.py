from django.shortcuts import render, redirect
from .forms import NewSlotForm
from utility.models import SingleSlot
from django.http import HttpResponse

# Sending user object to the form, to verify which fields to display/remove (depending on group)
def get_form_kwargs(self):
    kwargs = super(addSlot, self).get_form_kwargs()
    kwargs.update({'user': self.request.user})
    return kwargs
def addEvent(request):
    render(request, 'organizer/add_event.html')
def addSlot(request):
    is_organizer = False
    for g in request.user.groups.all():
        if g.name == 'Organizer':
            is_organizer = True
    if not is_organizer:
        return HttpResponse('You don\'t have the right permissions to see this page. You must be an Organizer to add slots.')
    if(request.method == 'POST'):
        form = NewSlotForm(request.POST, user=request.user)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.save()
    else:
        form = NewSlotForm(user=request.user)
    slots = SingleSlot.objects.all()
    return render(request, 'organizer/add_slot.html', {'form':form, 'slots':slots})
def index(requst):
    return redirect('/accounts/profile')
