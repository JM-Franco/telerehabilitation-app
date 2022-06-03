from django.db import models
from datetime import datetime
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Regex to validate ONLY Philippine numbers
phone_regex = RegexValidator(
    r"^(09|\+639)\d{9}$",
    message="Phone number must begin with +639 or 09 followed by a 9 digits",
)
# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email address.")
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
    email = models.EmailField(verbose_name="email", max_length=225, unique=True)
    first_name = models.CharField(
        verbose_name="first name", max_length=225, null=True, blank=True
    )
    last_name = models.CharField(
        verbose_name="last name", max_length=225, null=True, blank=True
    )
    birthdate = models.DateField(auto_now_add=False, null=True, blank=True)
    age = models.PositiveSmallIntegerField(
        null=True,
        blank=False,
        validators=[MaxValueValidator(200), MinValueValidator(0)],
    )
    sex = models.CharField(
        max_length=1, choices=[("M", "Male"), ("F", "Female")], null=True, blank=True
    )
    contact_number = models.CharField(
        max_length=13, validators=[phone_regex], null=True, blank=True
    )
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    role = models.CharField(
        verbose_name="role",
        max_length=2,
        choices=[
            ("SA", "System Admin"),
            ("PT", "Physical Therapist"),
            ("P", "Patient"),
        ],
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
  
class SystemAdminProfile(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name}"

class PhysicalTherapistProfile(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name}"

class PatientProfile(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name}"

class Clinic_Hours(models.Model):
    pt = models.ForeignKey(PhysicalTherapistProfile, default=None, on_delete=models.CASCADE)
    weekday = models.CharField(
        verbose_name="weekday",
        max_length=5,
        choices=[
            ('MON', 'Monday'),
            ('TUES', 'Tuesday'),
            ('WED', 'Wednesday'),
            ('THURS', 'Thursday'),
            ('FRI', 'Friday'),
            ('SAT', 'Saturday'),
            ('SUN', 'Sunday'),
        ],
        default='MON',
    )
    hours = ArrayField(ArrayField(models.TimeField(verbose_name='hours', auto_now_add=False)))

class Teleconsultation_Hours(models.Model):
    pt = models.ForeignKey(PhysicalTherapistProfile, default=None, on_delete=models.CASCADE)
    teleconsultation_weekday = models.CharField(max_length=9,choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', "Sunday")], default='MON')
    teleconsultation_hours = ArrayField(ArrayField(models.TimeField(verbose_name = 'teleconsultation_time', auto_now_add=False)))


class AppointmentManager(models.Manager):
    """ Event manager """

    def get_all_events(self):
        apt = Appointment.objects.filter(is_active=True, is_deleted=False)
        return apt

    def get_running_events(self):
        running_apt = Appointment.objects.filter(
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_apt

class Appointment(models.Model):
    patient= models.ForeignKey(PatientProfile, default=None, on_delete=models.CASCADE)
    pt = models.ForeignKey(PhysicalTherapistProfile, default=None, on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=[('teleconsultation', 'teleconsultation'), ('clinical', 'Clinical')], default='teleconsultation')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('reschedule', 'Reschedule'), ('cancelled', 'Cancelled'), ('finished', 'Finished')], default='pending')
    title = models.TextField(default="text title")
    description = models.TextField(default="text description")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    objects = AppointmentManager()
    @property
    def get_html_url(self):
        url = reverse('webapp:edit_appointment', args=(self.id,))
        return f'<a href="{url}">{self.patient.account.first_name.capitalize()} {self.patient.account.last_name.capitalize()} <br> {self.start_time.strftime("%I:%M %p")} - {self.end_time.strftime("%I:%M %p")} <br> Status: {self.status} <br> Type: {self.type} </a>'

class Messages(models.Model):
    receiver = models.ForeignKey(Account, default=None, on_delete=models.CASCADE, related_name='receiver')
    sender = models.ForeignKey(Account, default=None, on_delete=models.CASCADE, related_name='sender')
    subject = models.CharField(max_length=256, default='Subject')
    text = models.CharField(max_length=256, default='Hello')
    date_sent = models.DateTimeField(verbose_name='date sent', auto_now_add=True)


class AccountRequest(models.Model):
    email = models.EmailField(max_length=225)
    role = models.CharField(
        blank=True,
        verbose_name="role",
        max_length=2,
        choices=[
            ("SA", "System Admin"),
            ("PT", "Physical Therapist"),
            ("P", "Patient"),
        ],
    )
    status = models.CharField(
        max_length=8,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("denied", "Denied"),
        ],
        default="pending",
    )

    def __str__(self):
        return f"{self.email} - {self.role}"


class URLs(models.Model):
    pt = models.ForeignKey(PhysicalTherapistProfile, default=None, on_delete=models.CASCADE)
    urls = models.URLField(max_length=200)

    
class File(models.Model):
    filename = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='files/pdfs/')
    
    def __str__(self):
        return self.filename
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)

class Order(models.Model):
    patient = models.ForeignKey(PatientProfile, default=None, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='files/orders/')
    
    def __str__(self):
        return self.filename
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)

class Image(models.Model):
    image_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='files/', blank=True)
    
    def __str__(self):
        return self.image_title
    
   # def save(self, *args, **kwargs):
    #    img = Image.open(self.image.path)
        
    ##    if img.height > 400 or img.width > 400:
     ##       output_size = (400,400)
        
      #  img.thumbnail(output_size)
      #  img.save(self.image.path)
class Video(models.Model):
    name= models.CharField(max_length=500)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return f"{self.name}: {str(self.videofile)}"