from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "webapp"

urlpatterns = [
    path("", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("request_account/", views.request_account, name="request_account"),
    path(
        "request_account_sent/", views.request_account_sent, name="request_account_sent"
    ),
    path("profile_page/", views.profile_page, name="profile_page"),
    path("edit_profile/<int:pk>", views.edit_profile, name="edit_profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # SA-related
    path("account_requests/", views.account_requests, name="account_requests"),
    path("accounts/", views.accounts, name="accounts"),
    # PT-related
    path("calendar/", views.CalendarViewPT.as_view(), name="calendar"),
    path("calendar/new", views.appointment, name="new_appointment"),
    path("calendar/edit/(?P<event_id>\d+)/$", views.appointment, name="edit_appointment"),
    path("create_clinic_hours/<int:pk>", views.create_clinic_hours, name="create_clinic_hours"),
    path("edit_clinic_hours/<int:pk>", views.edit_clinic_hours, name="edit_clinic_hours"),
    path("delete_clinic_hours/<int:pk>", views.delete_clinic_hours, name="delete_clinic_hours"),
    path("patients/", views.patients, name="patients"),
    path("active_patients/", views.active_patients, name="active_patients"),
    path("active_patients/patients_profile/", views.patients_profile, name="patients_profile"),
    path("inactive_patients/", views.inactive_patients, name="inactive_patients"),
    path("appointments/", views.pt_appointments, name="pt_appointments"),
    path("remind_appointment/<int:pk>/<int:apt_id>", views.send_apt_reminder, name="pt_remind_apt"),
    path("teleconferencing/", views.teleconferencing, name="teleconferencing"),
    path("resources", views.resources, name="resources"),
    path("delete_url/<int:url_id>", views.delete_url, name="delete_url"),
    path('pt/messages/', views.pt_messages, name='pt_messages'),
    path('pt/messages/view_messages/<int:user_id>/', views.pt_view_messages, name='pt_view_messages'),
    path('pt/messages/view_messages_sent/<int:user_id>/', views.pt_view_messages_sent, name='pt_view_messages_sent'),
    path('pt/send_message/', views.pt_send_message, name='pt_send_message'),
    path("create_tc_hours/<int:pk>", views.create_tc_hours, name="create_tc_hours"),
    path("edit_tc_hours/<int:pk>", views.edit_tc_hours, name="edit_tc_hours"),
    path("delete_tc_hours/<int:pk>", views.delete_tc_hours, name="delete_tc_hours"),
    # P-related
    path("p_search/", views.p_search, name="p_search"),
    path("p_records/", views.p_records, name="p_records"),
    path('messages/', views.messages, name='messages'),
    path('messages/view_messages/<int:user_id>/', views.view_messages, name='view_messages'),
    path('messages/view_messages_sent/<int:user_id>/', views.view_messages_sent, name='view_messages_sent'),
    path('send_message/', views.send_message, name='send_message'),
    path('patient/appointments/', views.appointments_page, name='appointments_page'),
    path('physical_therapists/request_appointment/', views.request_appointment, name='request appointment'),
    path('physical_therapists/reschedule_appointment/<int:request_id>', views.resched_appointment, name='reschedule_appointment'),
    path('physical_therapists/', views.physical_therapists, name='physical_therapists'),
    path('physical_therapists/<int:user_id>/', views.view_profile_pt, name='view_profile_pt'),
    path('physical_therapists/appointment_hours/<int:user_id>/', views.view_pt_appointment_hours, name='view_pt_appointment_hours'),
    # Reset Password
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="webapp/password_reset/reset_password.html",
            success_url=reverse_lazy("webapp:password_reset_done"),
            email_template_name="webapp/password_reset/password_reset_email.html",
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="webapp/password_reset/reset_password_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="webapp/password_reset/reset_password_form.html",
            success_url=reverse_lazy("webapp:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="webapp/password_reset/reset_password_done.html"
        ),
        name="password_reset_complete",
    ),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='webapp/reset_password_form.html'), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='webapp/reset_password_done.html'), name='password_reset_complete')
    # HTMX
    path(
        "htmx/toggle_is_active/<int:pk>",
        views.toggle_is_active,
        name="toggle_is_active",
    ),
    path(
        "htmx/account_request_action/<str:action>/<int:pk>/",
        views.account_request_action,
        name="account_request_action",
    ),
        path(
        "htmx/appointments_request_action/<str:action>/<int:id>/",
        views.appointments_request_action,
        name="appointments_request_action",
    ),
    path(
        "htmx/account_requests_search/",
        views.account_requests_search,
        name="account_requests_search",
    ),
    path("htmx/accounts_search/", views.accounts_search, name="accounts_search"),
    path(
        "htmx/get_account_detail_view/<int:pk>",
        views.get_account_detail_view,
        name="get_account_detail_view",
    ),
    path("htmx/p_search_results/", views.p_search_results, name="p_search_results"),
]
