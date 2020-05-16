from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader


def index(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (DATA VIEWER)',
    }
    return render(request, 'data_viewer/index.html', context)