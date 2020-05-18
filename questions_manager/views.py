from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from howru_models.models import Question
# Create your views here.
from .forms import CreateQuestionForm, QuestionForm


@login_required(login_url="/login/")
def create(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            question = Question(text=form.cleaned_data.get("text"),
                                responses=form.cleaned_data.get("responses"),
                                public=form.cleaned_data.get("public"),
                                creator_id=request.user,
                                language=form.cleaned_data.get("language"))
            question.save()
            return index(request, new_context={"success_msg": "Question has been successfully created"})
    else:
        form = CreateQuestionForm()
    context = {
        'form': form,
    }
    return render(request, 'questions_manager/create.html', context)


@login_required(login_url="/login/")
def index(request, new_context={}):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    context.update(new_context)
    return render(request, 'questions_manager/index.html', context)


def delete(request, question_id):
    if request.method == "POST":
        Question.objects.get(id=question_id).delete()
        return index(request, new_context={"success_msg": "Question has been successfully deleted"})
    return render(request, 'questions_manager/delete.html')



def modify(request, question_id):
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=Question.objects.get(id=question_id))
        print("poooost")
        if form.is_valid():
            form.save()
            return index(request, new_context={"success_msg": "Question has been successfully modified"})
    else:
        form = QuestionForm(instance=Question.objects.get(id=question_id))
    return render(request, 'questions_manager/modify.html', context={"form": form})
