from django import template

from howru_models.models import PendingQuestion

register = template.Library()
@register.filter
def is_question_assigned(patient, question):
    try:
        patient.pendingquestion_set.get(question_id=question)
        return True
    except PendingQuestion.DoesNotExist:
        return False
