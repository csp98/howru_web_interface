# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("web_interface.authentication.urls")),
    path("", include("web_interface.app.urls")),
    path("patients_manager/", include("web_interface.patients_manager.urls")),
    path("questions_manager/", include("web_interface.questions_manager.urls"))
]
