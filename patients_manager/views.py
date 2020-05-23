from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.
from howru_models.models import Patient, Doctor, PendingQuestion
from patients_manager.forms import AssignPatientForm


@login_required(login_url="/login/")
def index(request):
    doctor = Doctor.objects.get(user=request.user)
    all_patients = doctor.patient_set.all().order_by('username')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_patients, settings.PAGE_SIZE)
    try:
        patients = paginator.page(page)
    except PageNotAnInteger:
        patients = paginator.page(1)
    except EmptyPage:
        patients = paginator.page(paginator.num_pages)
    request.session['patients_page'] = page
    context = {
        'patients': patients,
        'success_msg': request.session.pop('message', None)
    }
    return render(request, 'patients_manager/index.html', context)


@login_required(login_url="/login/")
def assign(request):
    not_found = False
    if request.method == "POST":
        form = AssignPatientForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('username')
                patient = Patient.objects.get(username__iexact=username)
                if patient in request.user.doctor.patient_set.all():
                    request.session['message'] = f'Patient {username} is already in your patients'
                else:
                    request.user.doctor.patient_set.add(patient)
                    request.session['message'] = f'Patient {username} has been successfully added'
                page = request.session.pop('patients_page', 1)
                return redirect(f'/patients_manager?page={page}')
            except Patient.DoesNotExist:
                not_found = True
    else:
        form = AssignPatientForm()
    return render(request, 'patients_manager/assign.html', context={"form": form, "not_found": not_found})


@login_required(login_url="/login/")
def unassign(request, patient_id):
    patient = Patient.objects.get(identifier=patient_id)
    context = {"patient": patient}
    if request.method == "POST":
        request.user.doctor.patient_set.remove(patient)
        request.session['message'] = f'Patient has been successfully unassigned'
        page = request.session.pop('patients_page', 1)
        return redirect(f'/patients_manager?page={page}')
    return render(request, 'patients_manager/unassign.html', context)


@login_required(login_url="/login/")
def assign_questions(request, patient_id):
    all_questions = request.user.doctor.assigned_questions.all().order_by('text')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_questions, settings.PAGE_SIZE)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    request.session['patient_questions_page'] = page
    context = {
        'patient': Patient.objects.get(identifier=patient_id),
        'questions': questions,
        'success_msg': request.session.pop('message', None)
    }
    return render(request, 'patients_manager/assign_questions.html', context)


@login_required(login_url="/login/")
def assign_question_to_patient(request, question_id, patient_id):
    pending_question = PendingQuestion(doctor_id=request.user.doctor,
                                       question_id_id=question_id,
                                       patient_id_id=patient_id,
                                       answering=False)
    pending_question.save()
    #request.session['message'] = "Question successfully assigned to patient"
    page = request.session.pop('patient_questions_page', 1)
    return redirect(f'/patients_manager/assign_questions/{patient_id}?page={page}')


@login_required(login_url="/login/")
def unassign_question_to_patient(request, question_id, patient_id):
    pending_question = PendingQuestion.objects.get(doctor_id=request.user.doctor, question_id_id=question_id,
                                                   patient_id_id=patient_id)
    pending_question.delete()
    #request.session['message'] = "Question successfully unassigned to patient"
    page = request.session.pop('patient_questions_page', 1)
    return redirect(f'/patients_manager/assign_questions/{patient_id}?page={page}')
