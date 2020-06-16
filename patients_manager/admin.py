from django.contrib import admin
# Register your models here.
from django.utils.html import format_html

from .models import Doctor
from .models import Patient


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_analyst')


class PatientAdmin(admin.ModelAdmin):
    @staticmethod
    def profile_picture(obj):
        return format_html(
            f'<img src="data:image/png;base64,{obj.picture}" style="border-radius: 50%;" height="40" width="30">')

    list_display = ('username', 'profile_picture', 'name', 'language', '_gender', 'schedule',)
    readonly_fields = ["profile_picture", ]


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
