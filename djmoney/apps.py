from django.apps import AppConfig


class MoneyConfig(AppConfig):
    name = "djmoney"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        pass
