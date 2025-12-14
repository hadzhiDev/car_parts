from django.db import models


class Sale(models.Model):
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")
    client = models.ForeignKey('sales.Client', on_delete=models.PROTECT, related_name='purchases', verbose_name="Клиент")

    def __str__(self):
        return f"Продажа {self.id} клиенту {self.client.full_name} на {self.sale_date}"
    
    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='items', verbose_name="Продажа")
    product = models.ForeignKey('main.Product', on_delete=models.PROTECT, related_name='sale_items', verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена продажи")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в продаже {self.sale.id}"
    
    class Meta:
        verbose_name = "Товар продажи"
        verbose_name_plural = "Товары продаж"


class Client(models.Model):
    full_name = models.CharField(max_length=50, verbose_name="ФИО")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Баланс", default=0.00)
    address = models.CharField(max_length=255, verbose_name="Адрес", blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} {self.phone_number}"
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"