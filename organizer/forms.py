from datetime import datetime, timezone
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import models

from utility.models import Event, Slot
from feed.models import Feed_Entry
from groups.models import Group


class NewSingleSlotForm(forms.Form):
    title = forms.CharField(label='Title', max_length=30, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    start = forms.DateTimeField(label='Start time', input_formats=['%Y-%m-%dT%H:%M'],
                                widget=forms.DateTimeInput(
                                    attrs={'type': 'datetime-local',
                                           'class': 'form-control'}))
    end = forms.DateTimeField(label='End time', input_formats=['%Y-%m-%dT%H:%M'],
                              widget=forms.DateTimeInput(
                                  attrs={'type': 'datetime-local',
                                         'class': 'form-control'}))

    location = forms.CharField(label='Location', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    city = forms.CharField(label='City', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    state = forms.CharField(label='State', max_length=2, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    zip_code = forms.IntegerField(label='Zip Code', widget=forms.NumberInput(
        attrs={'type': 'number',
               'max': '99999',
               'class': 'form-control'}))

    maxVolunteers = forms.IntegerField(label='# Slots', widget=forms.NumberInput(
        attrs={'type': 'number',
               'min': '1',
               'class': 'form-control'}))

    in_person = forms.BooleanField(label='In person', widget=forms.CheckboxInput(
        attrs={'type': 'checkbox',
               'class': 'form-control'}))

    TESTdateField = {'DateField': forms.DateInput(attrs={'id': 'datetimepicker12'})}

    user = models.User()
    datetime = datetime.now(timezone.utc)

    extraFields = forms.CharField(label='Extra Fields (Seperate w/ Commas)', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewSingleSlotForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_location(self):
        user = self.cleaned_data['location']
        return user

    def clean_address(self):
        user = self.cleaned_data['address']
        return user

    def clean_city(self):
        user = self.cleaned_data['city']
        return user

    def clean_state(self):
        user = self.cleaned_data['state']
        return user

    def clean_zip_code(self):
        user = self.cleaned_data['zip_code']
        return user

    def clean_maxVolunteers(self):
        description = self.cleaned_data['maxVolunteers']
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

    def clean_extra(self):
        a = self.cleaned_data['extraFields']
        print(a)
        ans = {}
        for i in a.split(','):
            ans[i] = '-'

        return ans

    def save(self, commit=True):
        event = Event(
            organizer=self.user,
            name=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            location=self.cleaned_data['location'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            zip_code=self.cleaned_data['zip_code'],
            in_person=self.cleaned_data['in_person'],
            maxVolunteers=self.cleaned_data['maxVolunteers'],
            extraFields=self.cleaned_data['extraFields'],
            minVolunteers=1,
            volunteers=None,
            start=self.cleaned_data['start'],
            end=self.cleaned_data['end'],
            is_single=True,
            type='singleSlot')
        return event


class NewEventForm(forms.Form):
    title = forms.CharField(label='Title', max_length=30, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))

    start = forms.DateTimeField(label='Start time', input_formats=['%Y-%m-%dT%H:%M'],
                                widget=forms.DateTimeInput(
                                    attrs={'type': 'datetime-local',
                                           'class': 'form-control'}))
    end = forms.DateTimeField(label='End time', input_formats=['%Y-%m-%dT%H:%M'],
                              widget=forms.DateTimeInput(
                                  attrs={'type': 'datetime-local',
                                         'class': 'form-control'}))

    location = forms.CharField(label='Location', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    city = forms.CharField(label='City', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    state = forms.CharField(label='State', max_length=2, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    zip_code = forms.IntegerField(label='Zip Code', widget=forms.NumberInput(
        attrs={'type': 'number',
               'max': '99999',
               'class': 'form-control'}))

    """maxVolunteers = forms.IntegerField(label='# Slots', widget=forms.NumberInput(
        attrs={'type': 'number',
               'min': '1',
               'class': 'form-control'}))"""
    user = models.User()
    parentGroup = models.Group()
    datetime = datetime.now(timezone.utc)

    """in_person = forms.BooleanField(label='In person', widget=forms.CheckboxInput(
        attrs={'type': 'checkbox',
               'class': 'form-control'}))"""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.parentGroup = kwargs.pop('parentGroup')
        super(NewEventForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_user(self):
        user = self.cleaned_data['user']
        return user

    def clean_parentGroup(self):
        parentGroup = self.cleaned_data['parentGroup']
        return parentGroup

    """def clean_maxVolunteers(self):
        description = self.cleaned_data['maxVolunteers']
        return description
    def clean_in_person(self):
        in_person = self.cleaned_data['in_person']"""

    def clean_location(self):
        user = self.cleaned_data['location']
        return user

    def clean_address(self):
        user = self.cleaned_data['address']
        return user

    def clean_city(self):
        user = self.cleaned_data['city']
        return user

    def clean_state(self):
        user = self.cleaned_data['state']
        return user

    def clean_zip_code(self):
        user = self.cleaned_data['zip_code']
        return user

    def clean_start(self):
        start = self.cleaned_data['start']
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        return end

    def feed_entry(self, commit=True):
        feed_entry = Feed_Entry(
            user=self.user,
            datetime=self.datetime,
            description="Created event \"" + self.cleaned_data['title'] + "\""
        )

        return feed_entry

    def save(self, commit=True):
        event = Event(
            organizer=self.user,
            parentGroup=self.parentGroup,
            name=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            location=self.cleaned_data['location'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            zip_code=self.cleaned_data['zip_code'],
            # in_person=self.cleaned_data['in_person'],
            # maxVolunteers=self.cleaned_data['maxVolunteers'],
            # minVolunteers=1,
            # volunteers=None,
            start=self.cleaned_data['start'],
            end=self.cleaned_data['end'], )
        # is_single=False,)
        return event


class UpdateEventForm(forms.Form):
    title = forms.CharField(label='Title', max_length=30, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))

    start = forms.DateTimeField(label='Start time', input_formats=['%Y-%m-%dT%H:%M'],
                                widget=forms.DateTimeInput(
                                    attrs={'type': 'datetime-local',
                                           'class': 'form-control'}))
    end = forms.DateTimeField(label='End time', input_formats=['%Y-%m-%dT%H:%M'],
                              widget=forms.DateTimeInput(
                                  attrs={'type': 'datetime-local',
                                         'class': 'form-control'}))

    location = forms.CharField(label='Location', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    city = forms.CharField(label='City', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    state = forms.CharField(label='State', max_length=2, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    zip_code = forms.IntegerField(label='Zip Code', widget=forms.NumberInput(
        attrs={'type': 'number',
               'max': '99999',
               'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.event_id = kwargs.pop('id')
        super(UpdateEventForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_location(self):
        user = self.cleaned_data['location']
        return user

    def clean_address(self):
        user = self.cleaned_data['address']
        return user

    def clean_city(self):
        user = self.cleaned_data['city']
        return user

    def clean_state(self):
        user = self.cleaned_data['state']
        return user

    def clean_zip_code(self):
        user = self.cleaned_data['zip_code']
        return user

    def clean_start(self):
        start = self.cleaned_data['start']
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        return end

    def feed_entry(self, commit=True):
        feed_entry = Feed_Entry(
            user=self.user,
            datetime=self.datetime,
            description="Updated event \"" + self.cleaned_data['title'] + "\""
        )

        return feed_entry

    def save(self, commit=True):
        return self.cleaned_data


class NewSlotForm(forms.Form):
    title = forms.CharField(label='Title', max_length=30, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control',
               'required': False}))

    start = forms.DateTimeField(label='Start time', input_formats=['%Y-%m-%dT%H:%M'],
                                widget=forms.DateTimeInput(
                                    attrs={'type': 'datetime-local',
                                           'class': 'form-control'}))
    end = forms.DateTimeField(label='End time', input_formats=['%Y-%m-%dT%H:%M'],
                              widget=forms.DateTimeInput(
                                  attrs={'type': 'datetime-local',
                                         'class': 'form-control'}))

    location = forms.CharField(label='Location', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))

    maxVolunteers = forms.IntegerField(label='# Slots', widget=forms.NumberInput(
        attrs={'type': 'number',
               'min': '1',
               'class': 'form-control'}))

    paymentPerHour = forms.DecimalField(label='Payment Per Hour', widget=forms.NumberInput(
        attrs={'type': 'number',
               'min': '0',
               'class': 'form-control'}))

    user = models.User()
    parentEvent = Event()
    datetime = datetime.now(timezone.utc)

    extraFields = forms.CharField(label='Extra Fields', required=False, max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'placeholder': '[Not required],[Field 2],[Field 3] ...',
               'class': 'form-control'}))

    """in_person = forms.BooleanField(label='In person', widget=forms.CheckboxInput(
        attrs={'type': 'checkbox',
               'class': 'form-control'}))"""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.parentEvent = kwargs.pop('parentEvent')
        super(NewSlotForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_user(self):
        user = self.cleaned_data['user']
        return user

    def clean_location(self):
        user = self.cleaned_data['location']
        return user

    def clean_start(self):
        start = self.cleaned_data['start']
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        return end

    def clean_maxVolunteers(self):
        maxVolunteers = self.cleaned_data['maxVolunteers']
        return maxVolunteers

    def clean_paymentPerHour(self):
        paymentPerHour = self.cleaned_data['paymentPerHour']
        return paymentPerHour

    def clean_extra(self):
        a = self.cleaned_data['extraFields']
        ans = {}
        for i in a.split(','):
            ans[i] = '-'

        return ans

    def save(self, commit=True):
        slot = Slot(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            parentEvent=self.parentEvent,
            start=self.cleaned_data['start'],
            end=self.cleaned_data['end'],
            location=self.cleaned_data['location'],
            minVolunteers=1,
            maxVolunteers=self.cleaned_data['maxVolunteers'],
            extraFields=self.cleaned_data['extraFields'].replace(" ", ""),
            paymentPerHour=self.cleaned_data['paymentPerHour']  # self.parentEvent.maxVolunteers,
            # title=self.cleaned_data['title'],
            # description=self.cleaned_data['description'],
            # location=self.cleaned_data['location'],
            # address=self.cleaned_data['address'],
            # city=self.cleaned_data['city'],
            # state=self.cleaned_data['state'],
            # zip_code=self.cleaned_data['zip_code']
        )
        return slot


class FieldForm(forms.Form):
    field = forms.CharField(label='field', max_length=30)

    def __init__(self, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)

    def save(self):
        return self.cleaned_data['field']


class UpdateSlotForm(forms.Form):
    title = forms.CharField(label='Title', max_length=30, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control',
               'required': False}))

    start = forms.DateTimeField(label='Start time', input_formats=['%Y-%m-%dT%H:%M'],
                                widget=forms.DateTimeInput(
                                    attrs={'type': 'datetime-local',
                                           'class': 'form-control'}))
    end = forms.DateTimeField(label='End time', input_formats=['%Y-%m-%dT%H:%M'],
                              widget=forms.DateTimeInput(
                                  attrs={'type': 'datetime-local',
                                         'class': 'form-control'}))

    location = forms.CharField(label='Location', max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))

    paymentPerHour = forms.DecimalField(label='Payment Per Hour', widget=forms.NumberInput(
        attrs={'type': 'number',
               'min': '0',
               'class': 'form-control'}))

    extraFields = forms.CharField(label='Extra Fields', required=False, max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'placeholder': '[Not required],[Field 2],[Field 3] ...',
               'class': 'form-control'}))

    user = models.User()
    parentEvent = Event()
    datetime = datetime.now(timezone.utc)

    def __init__(self, *args, **kwargs):
        self.slot_id = kwargs.pop('id')
        super(UpdateSlotForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_user(self):
        user = self.cleaned_data['user']
        return user

    def clean_location(self):
        user = self.cleaned_data['location']
        return user

    def clean_start(self):
        start = self.cleaned_data['start']
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        return end

    def clean_paymentPerHour(self):
        paymentPerHour = self.cleaned_data['paymentPerHour']
        return paymentPerHour

    def clean_extra(self):
        return self.cleaned_data['extraFields']

    def save(self, commit=True):
        return self.cleaned_data


class EditTimeForm(forms.Form):
    time = forms.DateTimeField(label='Time', input_formats=['%Y-%m-%dT%H:%M'],
                               widget=forms.DateTimeInput(
                                   attrs={'type': 'datetime-local',
                                          'class': 'form-control',
                                          'value': datetime.now().strftime("%Y-%m-%dT%H:%M")}))

    def __init__(self, *args, **kwargs):
        super(EditTimeForm, self).__init__(*args, **kwargs)

    def save(self):
        return self.cleaned_data['time']
