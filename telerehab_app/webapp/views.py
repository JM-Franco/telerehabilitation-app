from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Incorrect email or password')
    return render(request, 'webapp/login.html')

@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return redirect('/')


def request_account(request):
    return render(request, 'webapp/request_account.html')

def reset_password(request):
    return render(request, 'webapp/reset_password.html')

@login_required(login_url='/')
def profile_page(request):
    user = request.user
    data = {'user':user}
    return render(request, 'webapp/profile_page.html', data)

@login_required(login_url='/')
def dashboard(request):
    user = request.user
    data = {'user':user}
    return render(request, 'webapp/dashboard.html', data)

@login_required(login_url='/')
def patients(request):
    return render(request, 'webapp/patients.html')

@login_required(login_url='/')
def appointments(request):
    return render(request, 'webapp/appointments.html')

@login_required(login_url='/')
def teleconferencing(request):
    return render(request, 'webapp/teleconferencing.html')    

@login_required(login_url='/')
def resources(request):
    return render(request, 'webapp/resources.html')
