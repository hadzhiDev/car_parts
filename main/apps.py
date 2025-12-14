from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    verbose_name = "Склады и товары"

    def ready(self):
        import main.signals 
