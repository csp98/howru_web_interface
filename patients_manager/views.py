import csv
import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.

from howru_models.models import Patient, PendingQuestion
from patients_manager.forms import AssignPatientForm, ExportForm


@login_required(login_url="/login/")
def index(request):
    doctor = request.user.doctor
    if 'search' in request.GET:
        term = request.GET['search']
        all_patients = doctor.patient_set.filter(name__icontains=term).order_by('username')
    else:
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
        request.session['message'] = f'Patient {patient} has been successfully deleted'
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
    pending_question = PendingQuestion(doctor=request.user.doctor,
                                       question_id=question_id,
                                       patient_id=patient_id,
                                       answering=False)
    pending_question.save()
    # request.session['message'] = "Question successfully assigned to patient"
    page = request.session.pop('patient_questions_page', 1)
    return redirect(f'/patients_manager/assign_questions/{patient_id}?page={page}')


@login_required(login_url="/login/")
def unassign_question_to_patient(request, question_id, patient_id):
    pending_question = PendingQuestion.objects.get(doctor=request.user.doctor, question_id=question_id,
                                                   patient_id=patient_id)
    pending_question.delete()
    # request.session['message'] = "Question successfully unassigned to patient"
    page = request.session.pop('patient_questions_page', 1)
    return redirect(f'/patients_manager/assign_questions/{patient_id}?page={page}')


@login_required(login_url="/login/")
def view_data(request, patient_id):
    answered_questions_set = Patient.objects.get(identifier=patient_id).answeredquestion_set
    list_of_questions = dict()
    for answered_question in answered_questions_set.all():
        if answered_question.question not in list_of_questions.keys():
            responses = dict()
            dates = dict()
            for r in answered_questions_set.filter(question__text=answered_question.question.text).order_by(
                    'answer_date'):
                dates[r.answer_date.strftime("%d-%m-%y")] = r.response
            for response in answered_question.question.responses:
                responses[response] = answered_questions_set.filter(response=response,
                                                                    question=answered_question.question).count()
            list_of_questions[answered_question.question] = {
                "dates": dates,
                'responses': responses
            }
    context = {
        'list_of_questions': list_of_questions,
        'patient': Patient.objects.get(identifier=patient_id)
    }
    return render(request, 'patients_manager/view_data.html', context)


def create_csv(patients, file_path, start_date, end_date):
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Patient username", "Question", "Answer", "Date"])
        for patient in patients:
            for answered_question in patient.answeredquestion_set.filter(answer_date__lte=end_date,
                                                                         answer_date__gte=start_date):
                writer.writerow(
                    [patient, answered_question.question, answered_question.response, answered_question.answer_date])


def patients_to_csv(patients, doctor, start_date, end_date):
    filename = f'patients_{doctor}.csv'
    file_path = os.path.join(settings.CSV_DIR, filename)
    create_csv(patients, file_path, start_date, end_date)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + filename
        return response, file_path


@login_required(login_url="/login/")
def export(request):
    if request.method == "POST":
        form = ExportForm(request.user.doctor, request.POST)
        if form.is_valid():
            # Export file
            patients = form.cleaned_data.get('patients')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            patients, path = patients_to_csv(patients, request.user.doctor, start_date, end_date)
            os.remove(path)
            return patients
    else:
        form = ExportForm(request.user.doctor)
    context = {
        'form': form,
    }
    return render(request, 'patients_manager/export.html', context)
