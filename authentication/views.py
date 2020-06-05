# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth import authenticate, login, update_session_auth_hash
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from howru_models.models import Patient

from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)

    correct_credentials = True
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                correct_credentials = False

    return render(request, "accounts/login.html",
                  {"form": form, 'correct_credentials': correct_credentials})


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # If the doctor is an analyst, assign him/her all the patients in the system
            analyst = form.cleaned_data['is_analyst']
            form.instance.doctor.is_analyst = analyst
            if analyst:
                form.instance.doctor.patient_set.set(Patient.objects.all())
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required(login_url="/login/")
def change_password(request):
    """
    Allows an user to change his/her password
    """
    success = False
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            success = True
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,
        'success': success
    })

@login_required(login_url="/login/")
def delete_account(request):
    """
    Deletes a doctor from the system
    """
    if request.method == "POST":
        request.user.doctor.delete()
        request.user.delete()
        return redirect('/')
    context = {}
    return render(request, 'delete_account.html', context)
