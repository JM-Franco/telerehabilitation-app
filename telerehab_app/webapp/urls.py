from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'webapp'

urlpatterns = [
        path('', views.login_user, name='login'),
        path('logout/', views.logout_user, name='logout'),
        path('request_account/', views.request_account, name='request_account'),
        path('reset_password/', views.reset_password, name='reset_password'),
        path('profile_page/', views.profile_page, name='profile_page'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('patients/', views.patients, name='patients'),
        path('appointment/', views.appointments, name='appointments'),
        path('teleconferencing/', views.teleconferencing, name='teleconferencing'),
        path('resources', views.resources, name='resources'),
]

