from django.shortcuts import render, redirect

# Create your views here.
from .forms import CreateQuestionForm
from howru_models.Question import Question


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
            question.to_db()
            created = True
    form = CreateQuestionForm()

    context = {
        'form': form,
        "form_errors": form.errors.values(),
        "created": created
    }

    return render(request, 'questions_manager/create.html', context)


def modify(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/MODIFY)',
    }
    return render(request, 'questions_manager/modify.html', context)


def delete(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/DELETE)',
    }
    return render(request, 'questions_manager/delete.html', context)


def view(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/VIEW)',
    }
    return render(request, 'questions_manager/view.html', context)
