from django import forms


class AssignPatientForm(forms.Form):
    username = forms.CharField()

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['username'].replace('@', '')


class DeletePatientForm(forms.Form):
    delete_answered_questions = forms.CharField()

    def clean(self):
        self.cleaned_data['delete_answered_questions'] = self.cleaned_data['delete_answered_questions'] == "Yes"
