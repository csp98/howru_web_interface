from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('', views.index, name='index'),
    path('delete/<int:question_id>/', views.delete, name='delete'),
    path('modify/<int:question_id>/', views.modify, name='modify'),
]