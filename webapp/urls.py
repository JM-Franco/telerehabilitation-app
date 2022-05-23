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
    path("active_patients/", views.active_patients, name="active_patients"),
    path("inactive_patients/", views.inactive_patients, name="inactive_patients"),
    # PT-related
    path("patients/", views.patients, name="patients"),
    path("appointments/", views.appointments, name="appointments"),
    path("teleconferencing/", views.teleconferencing, name="teleconferencing"),
    path("resources", views.resources, name="resources"),
    # P-related
    path("p_search/", views.p_search, name="p_search"),
    path("p_records/", views.p_records, name="p_records"),
    path('messages/', views.messages, name='messages'),
    path('messages/view_messages/<int:user_id>/', views.view_messages, name='view_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('patient/appointments/', views.appointments_page, name='appointments'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('physical_therapists/request_appointment/', views.request_appointment, name='request appointment'),
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
