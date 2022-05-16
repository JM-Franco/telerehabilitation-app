from django.core.mail import send_mail
from .models import PhysicalTherapistProfile, PatientProfile


def update_account_request(sender, instance, created, **kwargs):
    if instance.status == "approved":
        send_mail(
            "Account Request Granted",
            "This is to notify you of the approval for your request for an account",
            None,
            [instance.email],
            fail_silently=False,
        )

    elif instance.status == "denied":
        send_mail(
            "Account Request Denied",
            "This is to notify you of the denial for your request for an account",
            None,
            [instance.email],
            fail_silently=False,
        )


def create_profile(sender, instance, created,  **kwargs):
    if created:
        if instance.role == "SA":
            pass
        elif instance.role == "PT":
            PhysicalTherapistProfile.objects.create(account=instance)
        else:
            PatientProfile.objects.create(account=instance)
