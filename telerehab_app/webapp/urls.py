from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'webapp'

urlpatterns = [
        path('', views.login_user, name='login'),
        path('request_account/', views.request_account, name='request_account'),
        path('reset_password/', views.reset_password, name='reset_password'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('profile_page/', views.profile_page, name='profile_page'),
]

