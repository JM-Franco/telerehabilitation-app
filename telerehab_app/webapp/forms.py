from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import *
from django.forms import ModelForm, ChoiceField

from .models import *


class AccountRequestForm(ModelForm):
    ROLE_CHOICES = (("PT", "Physical Therapist"), ("P", "Patient"))
    role = ChoiceField(choices=ROLE_CHOICES, widget=Select())

    class Meta:
        model = AccountRequest
        fields = ["email"]
        widgets = {
            "email": EmailInput(),
        }


class EditProfileForm(ModelForm):
    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "birthdate",
            "age",
            "sex",
            "contact_number",
        ]
        exclude = ["email"]
        widgets = {
            "first_name": TextInput(),
            "last_name": TextInput(),
            "birthdate": DateInput(),
            "age": NumberInput(),
            "sex": Select(),
            "contact_number": TextInput(),
        }
