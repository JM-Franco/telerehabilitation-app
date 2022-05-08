from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.core.mail import send_mail

from .models import *
from .forms import *
from .decorators import *

import re

# Create your views here.


@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == "SA":
                return redirect("/account_requests/")
            elif user.role == "PT":
                return redirect("/patients/")
            else:
                return redirect("/appointments/")

            # For future implementation of the dashboard
            # return redirect('/dashboard/')

        else:
            messages.error(request, "Incorrect email or password")
    return render(request, "webapp/login.html")


@login_required(login_url="/")
def logout_user(request):
    logout(request)
    return redirect("/")


def request_account(request):
    request_form = AccountRequestForm()
    if request.method == "POST":
        request_form = AccountRequestForm(request.POST)
        if request_form.is_valid():
            instance = request_form.save()
            # Send email notifying user about their request
            send_mail(
                "Account Request Sent",
                "This is to notify you that your request for an account has"
                " been sent",
                None,
                [instance.email],
                fail_silently=False,
            )
            return redirect("/request_account_sent/")
    data = {"request_form": request_form}
    return render(request, "webapp/request_account.html", data)


def request_account_sent(request):
    return render(request, "webapp/request_account_sent.html")


def reset_password(request):
    return render(request, "webapp/reset_password.html")


@login_required(login_url="/")
def profile_page(request):
    user = request.user
    data = {"user": user}
    return render(request, "webapp/profile_page.html", data)


@login_required(login_url="/")
def edit_profile(request, pk):
    edit_profile_form = EditProfileForm(instance=request.user)
    if request.method == "POST":
        prevpath = request.POST.get("prevpath")
        edit_profile_form = EditProfileForm(request.POST, instance=request.user)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            return redirect(prevpath)
        # code here
    data = {"edit_profile_form": edit_profile_form}
    return render(request, "webapp/edit_profile.html", data)


@login_required(login_url="/")
def dashboard(request):
    user = request.user
    data = {"user": user}
    return render(request, "webapp/dashboard.html", data)


# SA-related views


@login_required(login_url="/")
@allowed_users(allowed_roles=["SA"])
def account_requests(request):
    account_requests = AccountRequest.objects.filter(status="pending")
    data = {"account_requests": account_requests}
    return render(request, "webapp/system_admin/account_requests.html", data)


@login_required(login_url="/")
@allowed_users(allowed_roles=["SA"])
def accounts(request):
    accounts = Account.objects.all().order_by("-is_active")
    data = {"accounts": accounts}
    return render(request, "webapp/system_admin/accounts.html", data)


# PT-related views


@login_required(login_url="/")
def patients(request):
    return render(request, "webapp/physical_therapist/patients.html")


@login_required(login_url="/")
def appointments(request):
    return render(request, "webapp/physical_therapist/appointments.html")


@login_required(login_url="/")
def teleconferencing(request):
    return render(request, "webapp/physical_therapist/teleconferencing.html")


@login_required(login_url="/")
def resources(request):
    return render(request, "webapp/physical_therapist/resources.html")


# P related views


@login_required(login_url="/")
def p_search(request):
    return render(request, "webapp/patient/p_search.html")


@login_required(login_url="/")
def p_records(request):
    return render(request, "webapp/patient/p_records.html")


# @login_required(login_url='/')
# def messages(request):
#     return render(request, 'webapp/patient/p_search.html')


# HTMX


@require_POST
@login_required(login_url="/")
@allowed_users(allowed_roles=["SA"])
def toggle_is_active(request, pk):
    account = Account.objects.get(pk=pk)
    account.is_active = not account.is_active
    account.save()

    return HttpResponse()


@require_POST
@login_required(login_url="/")
@allowed_users(allowed_roles=["SA"])
def account_request_action(request, action, pk):
    account_request = AccountRequest.objects.get(pk=pk)
    temp_pass = re.search(r"\w+(?=@)", account_request.email).group()

    if not Account.objects.filter(email=account_request.email).exists():
        if action == "approve":
            Account.objects.create(
                email=account_request.email,
                role=account_request.role,
                password=temp_pass,
            )
            account_request.status = "approved"
            account_request.save(update_fields=["status"])
        elif action == "deny":
            account_request.status = "denied"
            account_request.save(update_fields=["status"])
    else:
        print("Invalid Action")

    return HttpResponse()


@require_GET
@login_required(login_url="/")
@allowed_users(allowed_roles=["SA"])
def account_requests_search(request):
    # Query all AccountRequest instances
    account_requests = AccountRequest.objects.all()

    print(request.GET)

    filter = request.GET.getlist("filter")
    textfilter = request.GET.get("textfilter")

    account_requests = account_requests.filter(role__in=filter, status__in=filter)
    if textfilter:
        account_requests = account_requests.filter(email__icontains=textfilter)

    data = {"account_requests": account_requests}
    print(data)
    return render(request, "partials/account_requests_search.html", data)


@require_GET
@login_required(login_url="/")
@allowed_users(allowed_roles=["SA"])
def accounts_search(request):
    # Query all Account instances
    accounts = Account.objects.all()

    # Get filter
    filter = request.GET.getlist("filter")
    textfilter = request.GET.get("textfilter")

    # Filter by role
    accounts = accounts.filter(role__in=filter)

    # Filter by is_active
    if "Active" in filter and "Inactive" not in filter:
        accounts = accounts.filter(is_active=True)
    elif "Inactive" in filter and "Active" not in filter:
        accounts = accounts.filter(is_active=False)
    elif "Active" not in filter and "Inactive" not in filter:
        accounts = None
    if textfilter:
        accounts = accounts.filter(
            Q(first_name__icontains=textfilter) | Q(last_name__icontains=textfilter)
        )

    data = {"accounts": accounts}
    return render(request, "partials/accounts_search.html", data)


@require_GET
@login_required(login_url="/")
# @allowed_users(allowed_roles=["SA", "P"])
def get_account_detail_view(request, pk):
    account = Account.objects.get(pk=pk)
    return render(request, "partials/get_account_detail_view.html", {"account": account})


@require_GET
@login_required(login_url="/")
@allowed_users(allowed_roles=["P"])
def p_search_results(request):
    pts = Account.objects.filter(role="PT")
    filter = request.GET.get("filter")
    pts = pts.filter(Q(first_name__icontains=filter) | Q(last_name__icontains=filter))
    data = {"pts": pts}
    return render(request, "partials/p_search_results.html", data)
