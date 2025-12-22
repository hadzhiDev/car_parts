from django.apps import AppConfig


class SaleConfig(AppConfig):
    name = 'apps.sales'
    verbose_name = "Продажи"

    def ready(self):
        import apps.sales.signals
