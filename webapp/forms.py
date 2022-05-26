from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import *
from django.forms import ModelForm, ChoiceField, CharField, HiddenInput, TimeField
from django.core.exceptions import ValidationError

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

class createClinicHoursForm(ModelForm):
    extra_field_count = CharField(widget=HiddenInput(), required=False)
    hours_start= TimeField(widget=TimeInput(), required=True)
    hours_end = TimeField(widget=TimeInput(), required=True)
    class Meta:
        model = Clinic_Hours
        fields = [
            "weekday",
            "hours",
        ]
        exclude = ['pt', 'hours']
        widgets = {
            "weekday": Select(),
        }

    def __init__(self, *args, **kwargs):
            extra_fields = kwargs.pop('extra', 0)
            # check if extra_fields exist. If they don't exist assign 0 to them
            if not extra_fields:
                extra_fields = 0

            super(createClinicHoursForm, self).__init__(*args, **kwargs)
            self.fields['extra_field_count'].initial = extra_fields

            for index in range(int(extra_fields)):
                # generate extra fields in the number specified via extra_fields
                self.fields['extra_field_{index}'.format(index=index)] = \
                    ModelForm.TimeInput(required=False)
    
    # validation called when there are extra fields
    def has_non_empty_extra_fields(self, hour_start, hour_end): 
        if hour_start == "" or hour_end == "":
            print("Time field is empty!")
            raise ValidationError("Time field is empty!")
        return True
