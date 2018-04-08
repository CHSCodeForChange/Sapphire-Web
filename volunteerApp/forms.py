from datetime import datetime, timezone
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import models

class FilterTimeForm(forms.Form):
    starttime = forms.DateTimeField(label='Start', input_formats=['%Y-%m-%d'],
    widget=forms.DateTimeInput(
        attrs={'type': 'date',
               'class': 'form-control',
               'value': datetime.now().strftime("%Y-%m-%d")}))

    endtime = forms.DateTimeField(label='End', input_formats=['%Y-%m-%d'],
    widget=forms.DateTimeInput(
        attrs={'type': 'date',
               'class': 'form-control',
               'value': datetime.now().strftime("%Y-%m-%d")}))

    def __init__(self, *args, **kwargs):
        super(FilterTimeForm, self).__init__(*args, **kwargs)


    def getStart(self):
        return self.cleaned_data['starttime']

    def getEnd(self):
        return self.cleaned_data['endtime']
