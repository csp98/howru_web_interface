from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from howru_models.models import Patient

@login_required(login_url="/login/")
def index(request):
    patients = list()
    patients.append(Patient(name="name", language="lang", gender="m", username="test"))
    context = {
        'patients': patients
    }
    return render(request, 'patients_manager/index.html', context)