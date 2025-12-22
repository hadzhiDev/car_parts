from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'apps.main'
    verbose_name = "Склады и товары"

    def ready(self):
        import apps.main.signals 
