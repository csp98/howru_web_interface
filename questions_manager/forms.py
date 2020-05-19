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
                response_list.append(response)
        if len(response_list) < 2:
            raise ValidationError("You must specify at least two possible responses")
        privacy = cd.get("privacy")
        self.cleaned_data['responses'] = response_list
        self.cleaned_data['public'] = privacy == "Public"

class QuestionForm(ModelForm):
    privacy = forms.CharField()
    class Meta:
        model = Question
        fields = ["text", "responses", "public", "language"]
    def clean(self):
        cd = self.cleaned_data
        print(cd)
        clean_responses = cd.get("responses")[0].replace('\r', '')
        if '\n' not in clean_responses:
            raise ValidationError("You must specify at least two possible responses")
        privacy = cd.get("privacy")
        self.cleaned_data['responses'] = clean_responses.split('\n')
        self.cleaned_data['public'] = privacy == "Public"