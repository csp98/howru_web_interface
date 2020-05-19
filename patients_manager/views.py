from base64 import b64encode

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from howru_models.models import Patient, Doctor
from patients_manager.forms import AssignPatientForm


@login_required(login_url="/login/")
def index(request, new_context={}):
    doctor = Doctor.objects.get(user=request.user)
    patients = doctor.patient_set.all()
    context = {
        'patients': patients,
    }
    context.update(new_context)
    return render(request, 'patients_manager/index.html', context)


@login_required(login_url="/login/")
def assign(request):
    not_found = False
    if request.method == "POST":
        form = AssignPatientForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('username')
                patient = Patient.objects.get(username=username)
                doctor = Doctor.objects.get(user=request.user)
                doctor.patient_set.add(patient)
                return index(request, new_context={
                    "success_msg": "Patient {} has been successfully added".format(username)})
            except Patient.DoesNotExist:
                not_found = True
    else:
        form = AssignPatientForm()
    return render(request, 'patients_manager/assign.html', context={"form": form, "not_found": not_found})
