from datetime import datetime, timezone
from django import forms
from utility.models import Slot, Event

from .helpers import get_dt

class FilterTimeForm(forms.Form):
    starttime = forms.DateTimeField(label='Start', input_formats=['%Y-%m-%d'],
    widget=forms.DateTimeInput(
        attrs={'type': 'date',
               'class': 'form-control',
               'value': get_dt().strftime("%Y-%m-%d")}))

    endtime = forms.DateTimeField(label='End', input_formats=['%Y-%m-%d'],
    widget=forms.DateTimeInput(
        attrs={'type': 'date',
               'class': 'form-control',
               'value': get_dt().strftime("%Y-%m-%d")}))

    def __init__(self, *args, **kwargs):
        super(FilterTimeForm, self).__init__(*args, **kwargs)


    def getStart(self):
        return self.cleaned_data['starttime']

    def getEnd(self):
        return self.cleaned_data['endtime']


class SearchForm(forms.Form):
    query = forms.CharField(label='', required=False, max_length=120, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control',
               'placeholder': 'Search'}))

    def clean_query(self):
        return self.cleaned_data['query']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        query = self.cleaned_data['query']
        return query
