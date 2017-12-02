from django.shortcuts import render, redirect
from .forms import NewSlotForm

# Sending user object to the form, to verify which fields to display/remove (depending on group)
def get_form_kwargs(self):
    kwargs = super(addSlot, self).get_form_kwargs()
    kwargs.update({'user': self.request.user})
    return kwargs
def addEvent(request):
    render(request, 'organizer/add_event.html')
def addSlot(request):
    if(request.method == 'POST'):
        form = NewSlotForm(request.POST, user=request.user)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.save()
    else:
        form = NewSlotForm(user=request.user)
    return render(request, 'organizer/add_slot.html', {'form':form})
def index(requst):
    return redirect('/accounts/profile')
