from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from howru_models.models import Question, Response


class QuestionForm(ModelForm):
    privacy = forms.CharField()
    to_all = forms.CharField()
    responses_field = forms.CharField()

    class Meta:
        model = Question
        fields = ["text", "public", "language", "priority", "frequency"]

    def clean(self):
        cd = self.cleaned_data
        clean_responses = cd.get("responses_field").replace('\r', '')
        response_list = list()
        for response in clean_responses.split('\n'):
            if response:
                clean_response = response.strip()
                if clean_response:
                    response_list.append(response)
        responses = list(dict.fromkeys(response_list))
        if len(responses) < 2:
            raise ValidationError("You must specify at least two different responses")
        self.cleaned_data['responses'] = [Response(order=response_list.index(r), text=r) for r in responses]
        privacy = cd.get("privacy")
        self.cleaned_data['public'] = privacy == "Public"
        self.cleaned_data['assigned_to_all'] = self.cleaned_data['to_all'] == "yes"
