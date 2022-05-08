from django.apps import AppConfig
from django.db.models.signals import post_save, pre_save


class WebappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "webapp"

    def ready(self):
        from . import signals
        from .models import AccountRequest

        post_save.connect(
            signals.update_account_request,
            sender=AccountRequest,
            dispatch_uid="unique_id",
        )

        pre_save.connect(signals.create_profile, sender=AccountRequest)
