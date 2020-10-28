import csv
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, CharField, Value
from django.db.models.functions import Cast, ExtractDay, ExtractMonth, ExtractYear, Concat
from django.http import HttpResponse
from django.shortcuts import render, redirect

from howru_models.models import Patient, PendingQuestion
from web_interface.patients_manager.forms import AssignPatientForm, ExportForm


# Create your views here.


@login_required(login_url="/login/")
def index(request):
    """
    Shows all assigned patients from the request's doctor. Allows pagination.
    Available options:
        - View data
        - Assign questions
        - Delete patient
    """
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
    """
    Assigns a patient to the request's doctor.
    Required param: username.
    Data clean: remove @ and case insensitive.
    """
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
                    # Assign assigned_to_all questions
                    questions = request.user.doctor.assigned_questions.filter(assigned_to_all=True)
                    for question in questions:
                        pending = PendingQuestion(doctor=request.user.doctor,
                                                  question=question,
                                                  patient=patient,
                                                  answering=False)
                        pending.save()
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
    """
    Removes a patient from request's doctor assigned patients
    :param patient_id (int)
    """
    patient = Patient.objects.get(identifier=patient_id)
    context = {"patient": patient}
    if request.method == "POST":
        request.user.doctor.patient_set.remove(patient)
        # Delete pending questions
        pending = PendingQuestion.objects.filter(patient=patient, doctor=request.user.doctor).delete()
        request.session['message'] = f'Patient {patient} has been successfully deleted'
        page = request.session.pop('patients_page', 1)
        return redirect(f'/patients_manager?page={page}')
    return render(request, 'patients_manager/unassign.html', context)


@login_required(login_url="/login/")
def assign_questions(request, patient_id):
    """
    Shows request's doctor questions that can be assigned to the patient.
    Avaliable options:
        - Assign/Unassign questions
    :param patient_id (int):
    """
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
    """
    Assigns a question to a patient bu creating a PendingQuestion
    :param question_id (int)
    :param patient_id (int)
    """
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
    """
    Unassigns a question to a patient by removing the corresponding PendingQuestion
    :param question_id (int)
    :param patient_id (int)
    """
    pending_question = PendingQuestion.objects.get(doctor=request.user.doctor, question_id=question_id,
                                                   patient_id=patient_id)
    pending_question.delete()
    # request.session['message'] = "Question successfully unassigned to patient"
    page = request.session.pop('patient_questions_page', 1)
    return redirect(f'/patients_manager/assign_questions/{patient_id}?page={page}')


@login_required(login_url="/login/")
def view_data(request, patient_id):
    """
    Shows answered questions data from a patient.
    :param patient_id (int):
    """
    answered_set = Patient.objects.get(identifier=patient_id).answeredquestion_set
    if 'search' in request.GET:
        term = request.GET['search']
        all_questions = answered_set.filter(question__text__icontains=term, doctor=request.user.doctor).values(
            'question', 'question__text').annotate(n=Count('response')).order_by('question')
    else:
        all_questions = answered_set.filter(doctor=request.user.doctor).values('question', 'question__text').annotate(
            n=Count('response')).order_by('question')

    page = request.GET.get('page', 1)
    paginator = Paginator(all_questions, settings.PAGE_SIZE)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    list_of_questions = dict()
    for question in questions:
        pie_data = list(
            all_questions.filter(question_id=question['question']).values('response__text',
                                                                          'response__order').annotate(
                n=Count('response')))
        line_data = list(all_questions.filter(question_id=question['question']).values('response', 'question').order_by(
            'answer_date').annotate(
            day=Cast(ExtractDay('answer_date'), CharField()),
            month=Cast(ExtractMonth('answer_date'), CharField()),
            year=Cast(ExtractYear('answer_date'), CharField()),
            date=Concat('day', Value('/'), 'month', Value('/'), 'year', output_field=CharField())).values(
            'response__text',
            'response__order',
            'date'))
        list_of_questions[question['question']] = {
            'pie_data': pie_data,
            'line_data': line_data
        }
    context = {
        'questions': questions,
        'list_of_questions': list_of_questions,
        'patient': Patient.objects.get(identifier=patient_id)
    }
    return render(request, 'patients_manager/view_data.html', context)


def create_csv(patients, file_path, start_date, end_date):
    """
    Creates a CSV file with patients data
    :param patients (list)
    :param file_path (str)
    :param start_date (datetime)
    :param end_date (datetime)
    """
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Patient username", "Question", "Answer", "Date"])
        for patient in patients:
            for answered_question in patient.answeredquestion_set.filter(answer_date__lte=end_date,
                                                                         answer_date__gte=start_date):
                writer.writerow([
                    patient,
                    answered_question.question,
                    answered_question.response,
                    answered_question.answer_date.strftime('%Y-%m-%d %H:%M:%S')
                ])


def patients_to_csv(patients, doctor, start_date, end_date):
    """
    Creates a CSV file with patients data and sends it to the user.
    :param patients (list)
    :param doctor (doctor)
    :param start_date (datetime)
    :param end_date (datetime)
    """
    filename = f'patients_{doctor}.csv'
    file_path = os.path.join(settings.CSV_DIR, filename)
    create_csv(patients, file_path, start_date, end_date)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + filename
        return response, file_path


@login_required(login_url="/login/")
def export(request):
    """
    Allows to select desired patients and start/end date to download a CSV file with all the information
    (patient name, question, answer and date)
    """
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
