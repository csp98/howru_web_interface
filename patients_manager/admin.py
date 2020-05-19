from django.contrib import admin

# Register your models here.
from .models import Doctor
from .models import Patient

admin.site.register(Patient)
admin.site.register(Doctor)