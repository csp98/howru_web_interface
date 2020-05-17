from django.contrib import admin

# Register your models here.
from questions_manager.models import AnsweredQuestion, PendingQuestion, Question

admin.site.register(Question)
admin.site.register(PendingQuestion)
admin.site.register(AnsweredQuestion)
