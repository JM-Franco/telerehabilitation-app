from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import *
from django.forms import ModelForm 

from .models import * 

# class AccountRequestForm(ModelForm):
    
class AccountActiveForm(ModelForm):
    class Meta:
        model = Account
        fields = ['is_active']
        widgets = {
            'is_active' : CheckboxInput()
        }