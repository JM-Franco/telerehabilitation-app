from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'webapp'

urlpatterns = [
        path('', views.login_user, name='login'),
        path('logout/', views.logout_user, name='logout'),
        path('request_account/', views.request_account, name='request_account'),
        path('profile_page/', views.profile_page, name='profile_page'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('patients/', views.patients, name='patients'),
        path('appointment/', views.appointments, name='appointments'),
        path('teleconferencing/', views.teleconferencing, name='teleconferencing'),
        path('resources', views.resources, name='resources'),

        # Reset Password
        path('reset_password/', auth_views.PasswordResetView.as_view(template_name='webapp/password_reset/reset_password.html', success_url=reverse_lazy('webapp:password_reset_done'), email_template_name='webapp/password_reset/password_reset_email.html'), name='reset_password'),
        path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='webapp/password_reset/reset_password_sent.html'), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='webapp/password_reset/reset_password_form.html', success_url=reverse_lazy('webapp:password_reset_complete')), name='password_reset_confirm'),
        path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='webapp/password_reset/reset_password_done.html'), name='password_reset_complete'),
        # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='webapp/reset_password_form.html'), name='password_reset_confirm'),
        # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='webapp/reset_password_done.html'), name='password_reset_complete')

]

