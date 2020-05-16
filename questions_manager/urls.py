from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('modify/', views.modify, name='modify'),
    path('delete/', views.delete, name='delete'),
    path('view/', views.view, name='view')
]