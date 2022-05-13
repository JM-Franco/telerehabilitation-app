from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from .decorators import *

import re

# Create your views here.

@unauthenticated_user
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
    if request.method == 'POST':
        acc_data = Account_Request()
        acc_data.email = request.POST.get('email')
        acc_data.role = request.POST.get('role')
        acc_data.save()
        return redirect('/')
    return render(request, 'webapp/request_account.html')

def reset_password(request):
    return render(request, 'webapp/reset_password.html')

@login_required(login_url='/')
def profile_page(request):
    user = request.user
    data = {'user':user}
    print(data)
    return render(request, 'webapp/profile_page.html', data)

@login_required(login_url='/')
def dashboard(request):
    user = request.user
    data = {'user':user}
    print(data)
    return render(request, 'webapp/dashboard.html', data)

# SA-related views

@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def account_requests(request):
    account_requests = Account_Request.objects.filter(status='pending')
    data = {'account_requests':account_requests}
    return render(request, 'webapp/system_admin/account_requests.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def accounts(request):
    accounts = Account.objects.all().order_by('-is_active')
    data = {'accounts':accounts}
    return render(request, 'webapp/system_admin/accounts.html', data)

# PT-related views

@login_required(login_url='/')
def patients(request):
    return render(request, 'webapp/physical_therapist/patients.html')

@login_required(login_url='/') 
def appointments(request):
    return render(request, 'webapp/physical_therapist/appointments.html')

@login_required(login_url='/')
def teleconferencing(request):
    return render(request, 'webapp/physical_therapist/teleconferencing.html')    

@login_required(login_url='/')
def resources(request):
    return render(request, 'webapp/physical_therapist/resources.html')

# P-related views

@login_required(login_url='/')
def appointments(request):
    return render(request, 'webapp/patient/appointments.html')

@login_required(login_url='/')
def physical_therapists(request):
    pt_accounts = Account.objects.filter(role="PT")
    data = {'pt_accounts':pt_accounts}
    #print(data)
    
    return render(request, 'webapp/patient/pt_accounts.html', data)

@login_required(login_url='/')
def view_profile_pt(request, user_id):
    pt_account = Account.objects.filter(id=user_id)
    data = {'pt_account':pt_account}
    #print(data)
    return render(request, 'webapp/patient/pt_profile_page.html', data)

@login_required(login_url='/')
def view_pt_appointment_hours(request, user_id):
    pt_account = Account.objects.filter(id=user_id).get()
    pt_fk = PhysicalTherapist.objects.filter(account_ptr_id=user_id).get()
    pt_clinical_hours_data = Clinic_Hours.objects.filter(fk_id=pt_fk.id).get()
    pt_teleconsultation_hours_data = Teleconsultation_Hours.objects.filter(fk_id=pt_fk.id).get()

    data = {'pt_account':pt_account, 'pt_clinical_hours_data':pt_clinical_hours_data, 'pt_teleconsultation_hours_data': pt_teleconsultation_hours_data}
    print(pt_teleconsultation_hours_data.start_tc_time)
    return render(request, 'webapp/patient/pt_appointment_page.html', data)

# HTMX

@require_POST
@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def toggle_is_active(request, pk):
    account = Account.objects.get(pk=pk)
    account.is_active = not account.is_active 
    account.save()

    return HttpResponse()

@require_POST
@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def account_request_action(request, action, pk):
    account_request = Account_Request.objects.get(pk=pk)
    #temp_pass = re.search(r'\w+(?=@)', account_request.email).group()
    temp_pass = "123456"
    if action == 'approve':
        account = Account(email=account_request.email, role=account_request.role, password=make_password(temp_pass))
        account_request.status = 'approved'
        account_request.save(update_fields=['status'])
        account.save()
        if account_request.role == 'P':
            account_fk = Patient.objects.create(account_ptr_id=account.id)
            account_fk.save()
        elif account_request.role == 'PT':
            account_fk = PhysicalTherapist.objects.create(account_ptr_id=account.id)
            account_fk.save()
        elif account_request.role == 'SA':
            account_fk = SystemAdmin.objects.create(account_ptr_id=account.id)
            account_fk.save()

    elif action == 'deny':
        account_request.status = 'denied'
        account_request.save(update_fields=['status'])

    return HttpResponse()


@require_GET
@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def account_requests_search(request):
    # Query all Account_Request instances
    account_requests = Account_Request.objects.all() 

    print(request.GET)

    filter = request.GET.getlist('filter')
    textfilter = request.GET.get('textfilter')

    account_requests = account_requests.filter(role__in=filter, status__in=filter)
    if textfilter:
        account_requests = account_requests.filter(email__icontains=textfilter)

    data = {'account_requests':account_requests}
    print(data)
    return render(request, 'partials/account_requests_search.html', data)


@require_GET
@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def accounts_search(request):
    # Query all Account instances
    accounts = Account.objects.all()

    # Get filter
    filter = request.GET.getlist('filter')
    textfilter = request.GET.get('textfilter')

    # Filter by role
    accounts = accounts.filter(role__in=filter)

    # Filter by is_active
    if 'Active' in filter and 'Inactive' not in filter:
        accounts = accounts.filter(is_active=True)
    elif 'Inactive' in filter and 'Active' not in filter:
        accounts = accounts.filter(is_active=False)
    elif 'Active' not in filter and 'Inactive' not in filter:
        accounts = None
    if textfilter:
        accounts = accounts.filter(Q(first_name__icontains=textfilter)|Q(last_name__icontains=textfilter))

    data = { 'accounts':accounts }
    return render(request, 'partials/accounts_search.html', data)
