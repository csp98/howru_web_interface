from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

@login_required(login_url="/login/")
def index(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (DATA VIEWER)',
    }
    return render(request, 'data_viewer/index.html', context)
