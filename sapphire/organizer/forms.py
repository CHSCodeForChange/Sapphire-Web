from django import forms
from django.core.exceptions import ValidationError

class NewEventForm(forms.Form):
    # Check current user for organizer permissions
    name = forms.CharField(label='Name', max_length=50)

class NewSlotForm(forms.Form):
    
