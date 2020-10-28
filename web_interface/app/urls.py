# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from web_interface.app import views

urlpatterns = [
    # Homepage
    path('', views.index, name='home'),
]
