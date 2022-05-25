from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_POST, require_GET
from django.core.mail import send_mail
from django.views import generic
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from .decorators import *
from .utils import *
import calendar
import re
import pytz
from datetime import timedelta, date
from datetime import datetime as dt
import datetime
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
            return redirect('/')
            #messages.error(request, "Incorrect email or password")
    return render(request, "webapp/login.html")

@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return redirect('/')


def request_account(request):
    request_form = AccountRequestForm()
    if request.method == "POST":
        request_form = AccountRequestForm(request.POST)
        print(request_form)
        if request_form.is_valid():
            instance = request_form.save()
            
            #Send email notifying user about their request
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
    return render(request, 'webapp/reset_password.html')

@login_required(login_url='/')
def profile_page(request):
    user = request.user
    data = {'user':user}
    print(data)
    return render(request, 'webapp/profile_page.html', data)

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

@login_required(login_url='/')
def dashboard(request):
    user = request.user
    data = {'user':user}
    print(data)
    return render(request, 'webapp/dashboard.html', data)

# SA-related views

@login_required(login_url="/")
@allowed_users(allowed_roles=["SA"])
def account_requests(request):
    account_requests = AccountRequest.objects.filter(status="pending")
    data = {"account_requests": account_requests}
    return render(request, "webapp/system_admin/account_requests.html", data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def accounts(request):
    accounts = Account.objects.all().order_by('-is_active')
    data = {'accounts':accounts}
    return render(request, 'webapp/system_admin/accounts.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def active_patients(request):
    accounts = Account.objects.all().objects.filter(is_active=True)
    data = {'active_patients':active_patients}
    return render(request, "webapp/system_admin/active_patients.html", data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['SA'])
def inactive_patients(request):
    accounts = Account.objects.all().objects.filter(is_active=True)
    data = {'inactive_patients':inactive_patients}
    return render(request, "webapp/system_admin/inactive_patients.html", data)

# PT-related views

@login_required(login_url='/')
def patients(request):
    return render(request, 'webapp/physical_therapist/patients.html')

@login_required(login_url='/')
@allowed_users(allowed_roles=['PT'])
def pt_appointments(request):
    pt = PhysicalTherapistProfile.objects.filter(account_id=request.user.id).get()
    appointments_requests = Appointment.objects.filter(pt_id = pt.id).exclude(Q(status="cancelled") | Q(status="finished"))
    
    # Check if appointment is done
    for apt in appointments_requests:
        # if true apt has passed
        if dt.now().utcnow().replace(tzinfo=pytz.UTC) + timedelta(hours=8) > apt.end_time + timedelta(hours=8):  
            apt.status = "finished"
            apt.save()

    data = {"appointments_requests": appointments_requests}
    return render(request, 'webapp/physical_therapist/appointments.html', data)

@require_POST
@login_required(login_url="/")
@allowed_users(allowed_roles=["PT"])
def appointments_request_action(request, action, id):
    appointment_request = Appointment.objects.get(id=id)
    if action == "approve":
        appointment_request.status = "accepted"
        appointment_request.save(update_fields=["status"])
    elif action == "reschedule":
        appointment_request.status = "reschedule"
        appointment_request.save(update_fields=["status"])
    elif action == "deny":
        appointment_request.status = "cancelled"
        appointment_request.save(update_fields=["status"])
    return HttpResponse()

@login_required(login_url='/')
def teleconferencing(request):
    return render(request, 'webapp/physical_therapist/teleconferencing.html')    

@login_required(login_url='/')
def resources(request):
    return render(request, 'webapp/physical_therapist/resources.html')

@login_required(login_url='/')
@allowed_users(allowed_roles=['PT'])
def pt_messages(request):
    messages_data = Messages.objects.filter(receiver_id = request.user.id).exclude(sender_id=request.user.id).distinct('receiver_id').order_by('receiver_id','-date_sent')
    data = {'messages':messages_data}
    return render(request, 'webapp/physical_therapist/messages.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['PT'])
def pt_send_message(request):
    if request.method == 'POST':
        data = Messages()
        data.subject = request.POST.get('subject')
        data.text = request.POST.get('text')
        patient = PatientProfile.objects.filter(id=request.POST.get('p_id')).get()
        data.receiver_id = patient.account.id
        data.sender_id = request.user.id
        data.save()
        return redirect('/')
    accounts = PatientProfile.objects.all()
    data = {'accounts':accounts}
    return render(request, 'webapp/physical_therapist/send_message.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['PT'])
def pt_view_messages(request, user_id):
    received_messages = Messages.objects.filter(sender_id = user_id).order_by('sender_id','date_sent').all()
    patient = f"{received_messages[0].sender.first_name.capitalize()} {received_messages[0].sender.last_name.capitalize()}"
    data = {'received_messages':received_messages, 'patient' : patient}
    print(patient)
    return render(request, 'webapp/physical_therapist/view_messages.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['PT'])
def pt_view_messages_sent(request, user_id):
    sent_messages = Messages.objects.filter(Q(receiver_id = user_id) & Q(sender_id = request.user.id) ).order_by('sender_id','date_sent').all()
    received_messages = Messages.objects.filter(sender_id = user_id).order_by('sender_id','date_sent').all()
    patient = f"{received_messages[0].sender.first_name.capitalize()} {received_messages[0].sender.last_name.capitalize()}"
    data = {"sent_messages" : sent_messages, 'patient' : patient, 'id' :user_id}
    return render(request, 'webapp/physical_therapist/view_messages_sent.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['PT'])
def appointment(request, event_id=None):
    instance = Appointment()
    if event_id:
        instance = get_object_or_404(Appointment, pk=event_id)
    else:
        instance = Appointment()
    
    form = AppointmentForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('webapp:calendar'))
    return render(request, 'webapp/physical_therapist/new_appointment.html', {'form': form})

class CalendarViewPT(generic.View):
    template_name = "webapp/physical_therapist/calendar.html"
    form_class = AppointmentForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        if request.user.role == "PT":
            pt = PhysicalTherapistProfile.objects.filter(account_id=request.user.id).get()
            appointments = Appointment.objects.filter(status="accepted").filter(pt_id = pt.id).exclude(status="cancelled")
        elif request.user.role == "P":
            p = PatientProfile.objects.filter(account_id=request.user.id).get()
            appointments = Appointment.objects.filter(status="accepted").filter(patient_id = p.id).exclude(status="cancelled")
        apt_list = []
        # start: '2020-09-16T16:00:00'
        for apt in appointments:
            print(apt.start_time)
            details = f"{apt.patient.account.first_name.capitalize()} {apt.patient.account.last_name.capitalize()} - {apt.type}"
            fixed_time_start = apt.start_time + timedelta(hours=8)
            fixed_time_end = apt.end_time + timedelta(hours=8)
            
            apt_list.append(
                {
                    "title": details,
                    "link":  apt.get_html_url,
                    "start": fixed_time_start.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": fixed_time_end.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
        context = {"events": apt_list}
        return render(request, self.template_name, context)


# P-related views

@login_required(login_url="/")
@allowed_users(allowed_roles=['P'])
def p_search(request):
    return render(request, "webapp/patient/p_search.html")

@login_required(login_url="/")
@allowed_users(allowed_roles=['P'])
def p_records(request):
    return render(request, "webapp/patient/p_records.html")

@login_required(login_url='/')
@allowed_users(allowed_roles=['P'])
def messages(request):
    messages_data = Messages.objects.filter(receiver_id = request.user.id).exclude(sender_id=request.user.id).distinct('receiver_id').order_by('receiver_id','-date_sent')
    data = {'messages':messages_data}
    return render(request, 'webapp/patient/messages.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['P'])
def send_message(request):
    if request.method == 'POST':
        print(request.POST.get('pt_id'))
        data = Messages()
        data.subject = request.POST.get('subject')
        data.text = request.POST.get('text')
        pt = PhysicalTherapistProfile.objects.filter(id=request.POST.get('pt_id')).get()
        data.receiver_id = pt.account.id
        data.sender_id = request.user.id
        data.save()
        return redirect(reverse('webapp:messages'))
    pt_accounts = PhysicalTherapistProfile.objects.all()
    data = {'pt_accounts':pt_accounts}
    return render(request, 'webapp/patient/send_message.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['P'])
def view_messages(request, user_id):
    #print('here')
    sent_messages = Messages.objects.filter(Q(receiver_id = user_id) & Q(sender_id = request.user.id) ).order_by('receiver_id','date_sent').all()
    received_messages = Messages.objects.filter(sender_id = user_id).order_by('sender_id','date_sent').all()
    doctor =  "Dr. " + received_messages[0].sender.first_name.capitalize() + " " +  received_messages[0].sender.last_name.capitalize()
    data = {'received_messages':received_messages, "sent_messages" : sent_messages, 'doctor' : doctor}
    return render(request, 'webapp/patient/view_messages.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['P'])
def view_messages_sent(request, user_id):
    sent_messages = Messages.objects.filter(Q(receiver_id = user_id) & Q(sender_id = request.user.id) ).order_by('sender_id','date_sent').all()
    received_messages = Messages.objects.filter(sender_id = user_id).order_by('sender_id','date_sent').all()
    doctor = f"{received_messages[0].sender.first_name.capitalize()} {received_messages[0].sender.last_name.capitalize()}"
    data = {"sent_messages" : sent_messages, 'doctor' : doctor, 'id' :user_id}
    return render(request, 'webapp/patient/view_messages_sent.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['P'])
def appointments_page(request):
    patient = PatientProfile.objects.filter(account_id=request.user.id).get()
    appointments_data = Appointment.objects.filter(patient_id = patient.id).exclude(Q(status="cancelled") | Q(status="finished"))

    # Check if appointment is done
    for apt in appointments_data:
        # if true apt has passed
        if dt.now().utcnow().replace(tzinfo=pytz.UTC) + timedelta(hours=8) > apt.end_time + timedelta(hours=8):  
            apt.status = "finished"
            apt.save()

    data = {'appointments':appointments_data}
    return render(request, 'webapp/patient/appointments.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['P'])
def request_appointment(request):
    user = request.user
    pt_accounts = Account.objects.filter(role="PT")
    data = {'pt_accounts':pt_accounts}

    if request.method == 'POST':
        data = Appointment()
        data.type = request.POST.get('appointment_type')
        pt_chosen = Account.objects.filter(id=request.POST.get('pt_chosen')).get() 
        data.patient_id = PatientProfile.objects.filter(account_id=user.id).get().id 
        data.pt_id = PhysicalTherapistProfile.objects.filter(account_id=pt_chosen.id).get().id
        
        # Temp fix
        data.start_time = request.POST.get('sched')
        data.end_time = request.POST.get('sched')
        data.save()
        return redirect(reverse('webapp:appointments_page'))

    return render(request, 'webapp/patient/request_appointment_page.html', data)

@login_required(login_url='/')
@allowed_users(allowed_roles=['P'])
def resched_appointment(request, request_id):
    appointment = Appointment.objects.get(id = request_id)

    if request.method == 'POST':
        appointment.type = request.POST.get('appointment_type')
    
        appointment.status = "pending"
        appointment.start_time = request.POST.get('sched')
        appointment.end_time = request.POST.get('sched') 
        appointment.save()
        return redirect(reverse('webapp:appointments_page'))

    return render(request, 'webapp/patient/reschedule_appointment_page.html')

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

    pt = PhysicalTherapistProfile.objects.filter(account_id=user_id).get()
    pt_clinical_hours_data = Clinic_Hours.objects.filter(pt_id=pt.id).get()
    pt_teleconsultation_hours_data = Teleconsultation_Hours.objects.filter(pt_id=pt.id).get()

    data = {'pt_account':pt.account_id, 'pt_clinical_hours_data':pt_clinical_hours_data, 'pt_teleconsultation_hours_data': pt_teleconsultation_hours_data}
    # Original id in Account
    print(type(pt.account_id))
    # print(user_id)
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
    print(account_request.role)
    if not Account.objects.filter(email=account_request.email).exists():
        if action == "approve":
            ac = Account.objects.create(
                email=account_request.email,
                role=account_request.role,
                password=make_password(temp_pass),
            )
            account_request.status = "approved"
            account_request.save(update_fields=["status"])

            if account_request.role == 'P':
                account_fk = PatientProfile.objects.create(account_id=ac.id)
                account_fk.save()
            elif account_request.role == 'PT':
                account_fk = PhysicalTherapistProfile.objects.create(account_id=ac.id)
                account_fk.save()
            elif account_request.role == 'SA':
                account_fk = SystemAdminProfile.objects.create(account_id=ac.id)
                account_fk.save()

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

