from datetime import datetime

import pytz
from django import forms
from django.core.exceptions import ValidationError

from howru_helpers import UTCTime
from howru_models.models import Patient


class AssignPatientForm(forms.Form):
    username = forms.CharField()

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['username'].replace('@', '')


class ExportForm(forms.Form):
    patients = forms.ModelMultipleChoiceField(queryset=None)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

    def __init__(self, doctor, *args, **kwargs):
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['patients'].queryset = doctor.patient_set.all()

    def clean(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        # Add time to dates
        self.cleaned_data['start_date'] = datetime(day=start_date.day, month=start_date.month, year=start_date.year,
                                                   hour=0, minute=0, second=0, tzinfo=pytz.UTC)
        self.cleaned_data['end_date'] = datetime(day=end_date.day, month=end_date.month, year=end_date.year, hour=0,
                                                 minute=0,second=0, tzinfo=pytz.UTC)
        if self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
            raise ValidationError("Start date must be before end date")
