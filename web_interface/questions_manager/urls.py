from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('my_questions/', views.my_questions, name='my_questions'),
    path('public_questions/', views.public_questions, name='public_questions'),
    path('delete/<int:question_id>/', views.delete, name='delete'),
    path('modify/<int:question_id>/', views.modify, name='modify'),
    path('assign/<int:question_id>/', views.assign, name='assign'),
]