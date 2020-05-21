import pytz
from django import template
from django.utils import timezone

from howru_models.models import PendingQuestion

register = template.Library()
@register.filter
def is_question_assigned(patient, question):
    try:
        patient.pendingquestion_set.get(question_id=question)
        return True
    except PendingQuestion.DoesNotExist:
        return False

@register.filter
def get_latest_answer_time(patient):
    try:
        timezone.activate(pytz.timezone('Europe/Madrid'))
        result = patient.answeredquestion_set.order_by('-answer_date')[0].answer_date
        # TODO make timezone a doctor attribute
    except IndexError:
        result =  "-"
    return result