from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

phone_regex = RegexValidator(r'^(09|\+639)\d{9}$', message='Phone number must begin with +639 or 09 followed by a 9 digits') # Regex to validate ONLY Philippine numbers

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email=self.normalize_email(email), password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length = 225, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=225, null=True, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=225, null=True, blank=True)
    birthdate = models.DateField(auto_now_add=False, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=False, validators=[MaxValueValidator(200), MinValueValidator(0)])
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    contact_number = models.CharField(max_length=13, validators=[phone_regex], null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    role = models.CharField(verbose_name='role', max_length=2, choices=[('SA', 'System Admin'), ('PT', 'Physical Therapist'), ('P', 'Patient')])
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class SystemAdmin(models.Model):
    account_ptr = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    
class PhysicalTherapist(models.Model):
    account_ptr = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    
class Patient(models.Model):
    account_ptr = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
  
class Clinic_Hours(models.Model):
    fk = models.ForeignKey(PhysicalTherapist, default=None, on_delete=models.CASCADE)
    start_clinic_time = models.DateTimeField(verbose_name='start clinic hours', auto_now_add=False)
    end_clinic_time = models.DateTimeField(verbose_name='end clinic hours', auto_now_add=False)

class Teleconsultation_Hours(models.Model):
    fk = models.ForeignKey(PhysicalTherapist, default=None, on_delete=models.CASCADE)
    start_tc_time = models.DateTimeField(verbose_name='start teleconsultation hours', auto_now_add=False)
    end_tc_time = models.DateTimeField(verbose_name='end teleconsultation hours', auto_now_add=False)

class Appointment(models.Model):
    patient_fk = models.ForeignKey(Patient, default=None, on_delete=models.CASCADE)
    pt_fk = models.ForeignKey(PhysicalTherapist, default=None, on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=[('teleconsultation', 'teleconsultation'), ('clinical', 'Clinical')], default='teleconsultation')
    status = models.CharField(max_length=9, choices=[('pending', 'Pending'), ('finished', 'Finished'), ('cancelled', 'Cancelled')], default='pending')

class Account_Request(models.Model):
    email = models.EmailField(max_length=225)
    role = models.CharField(verbose_name='role', max_length=2, choices=[('SA', 'System Admin'), ('PT', 'Physical Therapist'), ('P', 'Patient')])
    status = models.CharField(max_length=8, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending')
