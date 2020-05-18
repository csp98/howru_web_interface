from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assign/', views.assign, name='assign'),
]