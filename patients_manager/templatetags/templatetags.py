import pytz
from django import template
from django.utils import timezone

from howru_models.models import PendingQuestion

register = template.Library()
@register.filter
def is_question_assigned(patient, question):
    """
    Returns wether the question is assigned to the patient or not
    """
    return patient.pendingquestion_set.filter(question=question).exists()

@register.filter
def get_latest_answer_time(patient):
    """
    Retrieves the last answer time of a given patient applying timezone.
    """
    try:
        timezone.activate(pytz.timezone('Europe/Madrid'))
        result = patient.answeredquestion_set.order_by('-answer_date')[0].answer_date
    except IndexError:
        result =  "-"
    return result