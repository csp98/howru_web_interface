from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from howru_models.models import Question
# Create your views here.
from .forms import CreateQuestionForm


@login_required(login_url="/login/")
def create(request):
    created = False
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get("question_text")
            responses = form.cleaned_data.get("responses")
            print(responses)
            question = Question(text=question_text, responses=responses)
            question.save()
            created = True
    form = CreateQuestionForm()

    context = {
        'form': form,
        "form_errors": form.errors.values(),
        "created": created
    }

    return render(request, 'questions_manager/create.html', context)


@login_required(login_url="/login/")
def modify(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/MODIFY)',
    }
    return render(request, 'questions_manager/modify.html', context)


@login_required(login_url="/login/")
def delete(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/DELETE)',
    }
    return render(request, 'questions_manager/delete.html', context)


@login_required(login_url="/login/")
def view(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/VIEW)',
    }
    return render(request, 'questions_manager/view.html', context)
