# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")),  # add this
    path("", include("app.urls")),  # add this
    path("data_viewer/", include("data_viewer.urls")),
    path("patients_manager/", include("patients_manager.urls")),
    path("questions_manager/", include("questions_manager.urls"))
]
