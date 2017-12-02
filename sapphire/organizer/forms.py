from django import forms
from django.core.exceptions import ValidationError
from utility.models import SingleSlot
from django.contrib.auth import models

class NewEventForm(forms.Form):
    # Check current user for organizer permissions
    name = forms.CharField(label='Name', max_length=50)

class NewSlotForm(forms.Form):
    start = forms.DateTimeField(label='Start time')
    end = forms.DateTimeField(label='End time')
    title = forms.CharField(label='Title', max_length=30)
    description = forms.CharField(label='Description')
    in_person = forms.BooleanField(label='In person')
    TESTdateField = {'DateField': forms.DateInput(attrs={'id': 'datetimepicker12'})}
    user = models.User()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewSlotForm, self).__init__(*args, **kwargs)
    def clean_title(self):
        title = self.cleaned_data['title']
        return title
    def clean_description(self):
        description = self.cleaned_data['description']
        return description
    def clean_in_person(self):
        in_person = self.cleaned_data['in_person']
        return in_person
    def clean_user(self):
        user = self.cleaned_data['user']
        return user
    def clean_start(self):
        start = self.cleaned_data['start']
        return start
    def clean_end(self):
        end = self.cleaned_data['end']
        return end
    def save(self, commit=True):
        slot = SingleSlot(
            organizer=self.user,
            name=self.cleaned_data['title'],
            in_person=self.cleaned_data['in_person'],
            maxVolunteers=1,
            minVolunteers=1,
            volunteers=None,
            start=self.cleaned_data['start'],
            end=self.cleaned_data['end'])
        return slot
