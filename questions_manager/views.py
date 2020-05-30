from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from .forms import QuestionForm
from .models import Question, Doctor, PendingQuestion


@login_required(login_url="/login/")
def create(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.responses = form.cleaned_data.get('responses')
            form.instance.assigned_to_all = form.cleaned_data.get('assigned_to_all')
            form.instance.creator = request.user.doctor
            form.save()
            request.user.doctor.assigned_questions.add(form.instance)
            request.session['message'] = "Question has been successfully created"
            # If assigned to all, assign it to all doctor's patients
            if form.instance.assigned_to_all:
                all_patients = request.user.doctor.patient_set.all()
                for patient in all_patients:
                    pending_question = PendingQuestion(doctor=request.user.doctor,
                                                       question=form.instance,
                                                       patient=patient,
                                                       answering=False)
                    pending_question.save()
            page = request.session.pop('my_questions_page', 1)
            return redirect(f'/questions_manager/my_questions?page={page}')
    else:
        form = QuestionForm()
    context = {
        'form': form,
    }
    return render(request, 'questions_manager/create.html', context)


@login_required(login_url="/login/")
def my_questions(request):
    if 'search' in request.GET:
        term = request.GET['search']
        all_questions = request.user.doctor.assigned_questions.filter(text__icontains=term).order_by('text')
    else:
        all_questions = request.user.doctor.assigned_questions.all().order_by('text')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_questions, settings.PAGE_SIZE)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    request.session['my_questions_page'] = page
    context = {
        'questions': questions,
        'success_msg': request.session.pop('message', None)
    }
    return render(request, 'questions_manager/my_questions.html', context)


@login_required(login_url="/login/")
def public_questions(request):
    if 'search' in request.GET:
        term = request.GET['search']
        all_questions = request.user.doctor.assigned_questions.filter(text__icontains=term, public=True).order_by('text')
    else:
        all_questions = request.user.doctor.assigned_questions.filter(public=True).order_by('text')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_questions, settings.PAGE_SIZE)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    request.session['public_questions_page'] = page
    context = {
        'questions': questions,
        'success_msg': request.session.pop('message', None)
    }
    return render(request, 'questions_manager/public_questions.html', context)


@login_required(login_url="/login/")
def assign(request, question_id):
    question = Question.objects.get(id=question_id)
    question.doctor_set.add(request.user.doctor)
    question.save()
    if question.assigned_to_all:
        all_patients = request.user.doctor.patient_set.all()
        for patient in all_patients:
            pending_question = PendingQuestion(doctor=request.user.doctor,
                                               question=question,
                                               patient=patient,
                                               answering=False)
            pending_question.save()
    page = request.session.pop('public_questions_page', 1)
    return redirect(f'/questions_manager/public_questions?page={page}')


@login_required(login_url="/login/")
def delete(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {"question": question}
    if request.method == "POST":
        request.user.doctor.assigned_questions.remove(question)
        request.session['message'] = f'Question {question} has been successfully deleted'
        page = request.session.pop('my_questions_page', 1)
        return redirect(f'/questions_manager/my_questions?page={page}')
    return render(request, 'questions_manager/delete.html', context)


@login_required(login_url="/login/")
def modify(request, question_id):
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=Question.objects.get(id=question_id))
        if form.is_valid():
            form.instance.responses = form.cleaned_data.get('responses')
            form.instance.assigned_to_all = form.cleaned_data.get('assigned_to_all')
            form.save()
            request.session['message'] = f'Question {form.instance} has been successfully modified'
            # If assigned to all is checked, assign it to all patients
            if form.instance.assigned_to_all:
                all_patients = request.user.doctor.patient_set.all()
                for patient in all_patients:
                    PendingQuestion.objects.get_or_create(doctor=request.user.doctor,
                                                          question=form.instance,
                                                          patient=patient,
                                                          answering=False)
            # Otherwise, remove it from all patients
            else:
                all_patients = request.user.doctor.patient_set.all()
                for patient in all_patients:
                    PendingQuestion.objects.filter(doctor=request.user.doctor,
                                                   question=form.instance,
                                                   patient=patient
                                                   ).delete()

            page = request.session.pop('my_questions_page', 1)
            return redirect(f'/questions_manager/my_questions?page={page}')
    else:
        form = QuestionForm(instance=Question.objects.get(id=question_id))
    return render(request, 'questions_manager/modify.html', context={"form": form})
