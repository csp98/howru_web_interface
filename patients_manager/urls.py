from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assign/', views.assign, name='assign'),
    path('unassign/<int:patient_id>/', views.unassign, name='unassign'),
    path('assign_questions/<int:patient_id>/', views.assign_questions, name='assign_questions'),
    path('assign_questions/<int:question_id>/<int:patient_id>/', views.assign_question_to_patient,
         name='assign_question_to_patient'),
    path('unassign_questions/<int:question_id>/<int:patient_id>/', views.unassign_question_to_patient,
         name='unassign_question_to_patient'),
    path('view_data/<int:patient_id>/', views.view_data, name='view_data'),
    path('export/', views.export, name='export'),

]
