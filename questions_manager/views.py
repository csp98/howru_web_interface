from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from .forms import QuestionForm
from .models import Question, Doctor


@login_required(login_url="/login/")
def create(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.responses = form.cleaned_data.get('responses')
            form.instance.creator_id = request.user.doctor
            form.save()
            request.user.doctor.assigned_questions.add(form.instance)
            request.session['message'] = "Question has been successfully created"
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
    doctor = Doctor.objects.get(user=request.user)
    all_questions = Question.objects.filter(
        # ~Q(creator_id=doctor) &
        Q(public=True)
    ).order_by('text')
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
    #request.session['message'] = "Question has been successfully modified"
    page = request.session.pop('public_questions_page', 1)
    return redirect(f'/questions_manager/public_questions?page={page}')


@login_required(login_url="/login/")
def delete(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {"question": question}
    if request.method == "POST":
        request.user.doctor.assigned_questions.remove(question)
        request.session['message'] = "Question has been successfully deleted"
        page = request.session.pop('my_questions_page', 1)
        return redirect(f'/questions_manager/my_questions?page={page}')
    return render(request, 'questions_manager/delete.html', context)


@login_required(login_url="/login/")
def modify(request, question_id):
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=Question.objects.get(id=question_id))
        if form.is_valid():
            form.instance.responses = form.cleaned_data.get('responses')
            form.save()
            request.session['message'] = "Question has been successfully modified"
            page = request.session.pop('my_questions_page', 1)
            return redirect(f'/questions_manager/my_questions?page={page}')
    else:
        form = QuestionForm(instance=Question.objects.get(id=question_id))
    return render(request, 'questions_manager/modify.html', context={"form": form})
