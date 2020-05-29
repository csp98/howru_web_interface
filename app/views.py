# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

import pytz
from django import template
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

from howru_models.models import AnsweredQuestion, Question, Patient


def get_total_answers(doctor):
    total_answers = 0
    for patient in doctor.patient_set.all():
        total_answers += AnsweredQuestion.objects.filter(doctor_id=doctor, patient_id=patient).count()
    return total_answers


def get_top_patients(doctor):
    """ #TODO it gets the latest answers
    Retrieves the 5 users with most answered questions
    """
    top_patients = (
        doctor.patient_set.annotate(num_ans=Count('answeredquestion')).order_by('-num_ans')[:5]
    )
    result = [
        (patient, patient.num_ans) for patient in top_patients
    ]
    return result


def get_gender_stats(doctor, total_patients):
    if not total_patients:
        male_percentage = female_percentage = other_percentage = 0
    else:
        male_patients = doctor.patient_set.filter(_gender="M").count()
        female_patients = doctor.patient_set.filter(_gender="F").count()
        other_patients = doctor.patient_set.filter(_gender="O").count()
        male_percentage = round(male_patients * 100 / total_patients, 2)
        female_percentage = round(female_patients * 100 / total_patients, 2)
        other_percentage = round(other_patients * 100 / total_patients, 2)
    return male_percentage, female_percentage, other_percentage


def get_answers_per_hour(doctor):
    """
    Gets the percentage of answers depending on the hour
    :param doctor:
    :return (list): 0-3:59, 4:00-7:59, 8:00-11:59, 12:00-15:59, 16:00-19:59, 20:00-23:59
    """
    timezone.activate(pytz.timezone('Europe/Madrid'))
    number_of_answers = [
        AnsweredQuestion.objects.filter(doctor_id=doctor, answer_date__hour__gte=0,
                                        answer_date__hour__lt=4).count(),
        AnsweredQuestion.objects.filter(doctor_id=doctor, answer_date__hour__gte=4,
                                        answer_date__hour__lt=8).count(),
        AnsweredQuestion.objects.filter(doctor_id=doctor, answer_date__hour__gte=8,
                                        answer_date__hour__lt=12).count(),
        AnsweredQuestion.objects.filter(doctor_id=doctor, answer_date__hour__gte=12,
                                        answer_date__hour__lt=16).count(),
        AnsweredQuestion.objects.filter(doctor_id=doctor, answer_date__hour__gte=16,
                                        answer_date__hour__lt=20).count(),
        AnsweredQuestion.objects.filter(doctor_id=doctor, answer_date__hour__gte=20,
                                        answer_date__hour__lt=24).count()
    ]
    total = sum(number_of_answers)
    percentages = [round(number * 100 / total, 2) for number in number_of_answers] if total else 0
    return percentages


@login_required(login_url="/login/")
def index(request):
    doctor = request.user.doctor
    top_patients = get_top_patients(doctor)
    doctor_patients = doctor.patient_set
    number_associated_patients = doctor_patients.count()
    submitted_questions = Question.objects.filter(creator_id=doctor).count()
    total_answers = get_total_answers(doctor)
    male_percentage, female_percentage, other_percentage = get_gender_stats(doctor, number_associated_patients)
    answers_per_hour = get_answers_per_hour(doctor)

    context = {
        "top_patients": top_patients,
        "number_associated_patients": number_associated_patients,
        "submitted_questions": submitted_questions,
        "total_answers": total_answers,
        "male_percentage": male_percentage,
        "female_percentage": female_percentage,
        "other_percentage": other_percentage,
        "answers_per_hour": answers_per_hour
    }
    return render(request, "index.html", context)

@login_required(login_url="/login/")
def change_password(request):
    # TODO
    context = {}
    return render(request, "change_password.html", context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('error-500.html')
        return HttpResponse(html_template.render(context, request))
