from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from howru_models.models import Question

PRIVACY_OPTIONS = ["Public", "Private"]
LANGUAGES = ["English", "Spanish"]


class CreateQuestionForm(forms.Form):
    text = forms.CharField()
    responses = forms.CharField()
    privacy = forms.CharField()
    language = forms.CharField()

    def clean(self):
        cd = self.cleaned_data
        clean_responses = cd.get("responses").replace('\r', '')
        response_list = list()
        for response in clean_responses.split('\n'):
            if response:
                clean_response = response.strip()
                if clean_response:
                    response_list.append(response)
        if len(response_list) < 2:
            raise ValidationError("You must specify at least two possible responses")
        privacy = cd.get("privacy")
        self.cleaned_data['responses'] = response_list
        self.cleaned_data['public'] = privacy == "Public"

class QuestionForm(ModelForm):
    privacy = forms.CharField()
    responses_field = forms.CharField()
    class Meta:
        model = Question
        fields = ["text", "public", "language"]
    def clean(self):
        cd = self.cleaned_data
        clean_responses = cd.get("responses_field").replace('\r', '')
        response_list = list()
        for response in clean_responses.split('\n'):
            if response:
                clean_response = response.strip()
                if clean_response:
                    response_list.append(response)
        if len(response_list) < 2:
            raise ValidationError("You must specify at least two possible responses")
        self.cleaned_data['responses'] = response_list
        privacy = cd.get("privacy")
        self.cleaned_data['public'] = privacy == "Public"

class DeleteQuestionForm(forms.Form):
    delete_for_others = forms.CharField()

    def clean(self):
        delete_for_others = self.cleaned_data.get('delete_for_others')
        self.cleaned_data["delete_for_others"] = delete_for_others == "Yes"