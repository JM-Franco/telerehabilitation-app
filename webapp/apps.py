from django.apps import AppConfig
from django.db.models.signals import post_save


class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapp'

    def ready(self):
        from . import signals
        from .models import Account_Request
        post_save.connect(signals.update_account_request, sender=Account_Request, dispatch_uid='unique_id')
