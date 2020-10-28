from django.contrib import admin

# Register your models here.
from web_interface.questions_manager.models import AnsweredQuestion, PendingQuestion, Question, Response
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

class QuestionAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('text', 'creator')

class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'doctor', 'patient')

class PendingQuestionAdmin(JournalEntryAdmin):
    list_display = JournalEntryAdmin.list_display + ('answering',)

class AnsweredQuestionAdmin(JournalEntryAdmin):
    list_display = JournalEntryAdmin.list_display + ('response', 'answer_date' )

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'text')

admin.site.register(Question, QuestionAdmin)
admin.site.register(PendingQuestion, PendingQuestionAdmin)
admin.site.register(AnsweredQuestion, AnsweredQuestionAdmin)
admin.site.register(Response, ResponseAdmin)

