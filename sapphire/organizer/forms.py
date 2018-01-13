from django import forms
from django.core.exceptions import ValidationError
from utility.models import Event, Slot
from django.contrib.auth import models

class NewSingleSlotForm(forms.Form):
    start = forms.DateTimeField(label='Start time', widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local',
               'class': 'form-control'}))
    end = forms.DateTimeField(label='End time', widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local',
               'class': 'form-control'}))
    title = forms.CharField(label='Title', max_length=30, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))

    in_person = forms.BooleanField(label='In person', widget=forms.CheckboxInput(
        attrs={'type': 'checkbox',
               'class': 'form-control'}))

    TESTdateField = {'DateField': forms.DateInput(attrs={'id': 'datetimepicker12'})}

    user = models.User()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewSingleSlotForm, self).__init__(*args, **kwargs)
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
        event = Event(
            organizer=self.user,
            name=self.cleaned_data['title'],
            in_person=self.cleaned_data['in_person'],
            maxVolunteers=1,
            minVolunteers=1,
            volunteers=None,
            start=self.cleaned_data['start'],
            end=self.cleaned_data['end'],
            is_single=True)
        return event
class NewEventForm(forms.Form):
    title = forms.CharField(label='Title', max_length=30)
    location = forms.CharField(label='Location', max_length=240)
    user = models.User()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewEventForm, self).__init__(*args, **kwargs)
    def clean_title(self):
        title = self.cleaned_data['title']
        return title
    def clean_user(self):
        user = self.cleaned_data['user']
        return user
    def clean_location(self):
        location = self.cleaned_data['location']
        return location
    def save(self, commit=True):
        event = Event(
            organizer=self.user,
            name=self.cleaned_data['title'],
            location=self.cleaned_data['location'],
            in_person=None,
            maxVolunteers=None,
            minVolunteers=None,
            volunteers=None,
            start=None,
            end=None,
            is_single=False)
        return event
