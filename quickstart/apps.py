from django.apps import AppConfig
import os


class QuickstartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quickstart"
    
    def ready(self):
        from . import deamon

        if os.environ.get('RUN_MAIN', None) != 'true':
            deamon.start_scheduler()