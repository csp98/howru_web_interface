from django import forms
from django.core.exceptions import ValidationError

PRIVACY_OPTIONS = ["Public", "Private"]
LANGUAGES = ["English", "Spanish"]


class CreateQuestionForm(forms.Form):
    question_text = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Question text, for example: ¿How do you feel today?",
                "class": "form-control"
            }
        ))
    responses = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Question possible answers (one per line). For example:\nHappy\nSad\nTired\nAngry",
                "class": "form-control"
            }
        ))
    """
    privacy = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Private, Public",
                "class": "form-control"
            }
        ))
    language = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "English, Spanish",
                "class": "form-control"
            }
        ))
        """

    def clean(self):
        cd = self.cleaned_data
        clean_responses = cd.get("responses").replace('\r', '')
        if '\n' not in clean_responses:
            raise ValidationError("You must specify at least two possible responses")
        self.cleaned_data['responses'] = clean_responses.split('\n')
