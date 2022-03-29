from django.shortcuts import render
from .models import *

# Create your views here.

def login_user(request):
    return render(request, 'webapp/login.html')

def request_account(request):
    return render(request, 'webapp/request_account.html')

def reset_password(request):
    return render(request, 'webapp/reset_password.html')

def dashboard(request):
    return render(request, 'webapp/dashboard.html')

def profile_page(request):
    user = request.user
    data = {'user':user}
    return render(request, 'webapp/profile_page.html', data)
