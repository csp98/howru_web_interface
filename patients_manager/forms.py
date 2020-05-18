from django import forms


class AssignPatientForm(forms.Form):
    username = forms.CharField()

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['username'].replace('@', '')
