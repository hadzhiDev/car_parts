from django.apps import AppConfig


class SaleConfig(AppConfig):
    name = 'sales'
    verbose_name = "Продажи"

    def ready(self):
        import sales.signals  # noqa
