from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import models

from groups.models import Group

class NewGroupForm(forms.Form):
    name = forms.CharField(label='Title', max_length=120, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    tagline = forms.CharField(label='Tagline', max_length=120, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    description = forms.CharField(label='Description', max_length=960, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    website = forms.URLField(label='Website URL', widget=forms.URLInput(
        attrs={'class': 'form-control'}))


    location = forms.CharField(label='Location', max_length=240, widget=forms.TextInput(
        attrs={ 'type': 'text',
                'class': 'form-control'}))
    address = forms.CharField(label='Address', max_length=240, widget=forms.TextInput(
        attrs={ 'type': 'text',
                'class': 'form-control'}))
    city = forms.CharField(label='City', max_length=240, widget=forms.TextInput(
        attrs={ 'type': 'text',
                'class': 'form-control'}))
    state = forms.CharField(label='State', max_length=2, widget=forms.TextInput(
        attrs={ 'type': 'text',
                'class': 'form-control'}))
    zip_code = forms.IntegerField(label='Zip Code', widget=forms.NumberInput(
        attrs={ 'type': 'number',
                'max': '99999',
                'class': 'form-control'}))


    owner = models.User()

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        super(NewGroupForm, self).__init__(*args, **kwargs)
    def clean_name(self):
        title = self.cleaned_data['name']
        return title
    def clean_description(self):
        description = self.cleaned_data['description']
        return description
    def clean_tagline(self):
        tagline = self.cleaned_data['tagline']
        return tagline
    def clean_email(self):
        email = self.cleaned_data['email']
        return email
    def clean_website(self):
        website = self.cleaned_data['website']
        return website


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

    def clean_owner(self):
        owner = self.cleaned_data['owner']
        return owner


        return feed_entry
    def save(self, commit=True):
        group = Group(
            name=self.cleaned_data['name'],
            tagline=self.cleaned_data['tagline'],
            description=self.cleaned_data['description'],
            email=self.cleaned_data['email'],
            website=self.cleaned_data['website'],
            owner=self.owner,
            location=self.cleaned_data['location'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            zip_code=self.cleaned_data['zip_code'],
            )
        return group
