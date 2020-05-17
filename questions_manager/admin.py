from django.contrib import admin

# Register your models here.
from questions_manager.models import AnsweredQuestion, PendingQuestion, Question
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

class QuestionAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass
admin.site.register(Question, QuestionAdmin)
admin.site.register(PendingQuestion)
admin.site.register(AnsweredQuestion)

