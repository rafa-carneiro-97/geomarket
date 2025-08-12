from django.apps import AppConfig


class BusinessConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.business"
    verbose_name = "Negócio"

    def ready(self):
        # This will run the signals
        import apps.business.signals
