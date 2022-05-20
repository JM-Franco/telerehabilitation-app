from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import *
from django.forms import ModelForm, ChoiceField

from .models import *


class AccountRequestForm(ModelForm):
    ROLE_CHOICES = (("PT", "Physical Therapist"), ("P", "Patient"))
    role = ChoiceField(choices=ROLE_CHOICES, widget=Select())

    class Meta:
        model = AccountRequest
        fields = ["email", "role"]
        widgets = {
            "email": EmailInput(),
            "email": TextInput(),
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

class AppointmentForm(ModelForm):
  class Meta:
    model = Appointment
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(AppointmentForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)