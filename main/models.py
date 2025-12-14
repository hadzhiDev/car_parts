from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название страны")
    flag_image = models.ImageField(upload_to='country_flags/', verbose_name="Флаг страны")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название марки")
    logo = models.ImageField(upload_to='brand_logos/', verbose_name="Логотип марки")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    article_number = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='products', verbose_name="Склад")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Себестоимость", 
                                     null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена продажи", 
                                        null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name="Бренд", 
                              null=True, blank=True)
    country_of_origin = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='products', 
                                          verbose_name="Страна происхождения", null=True, blank=True)
    suits_for = models.CharField(max_length=200, verbose_name="Подходит для", null=True, blank=True,
                                 help_text="Укажите модели автомобилей, для которых подходит эта запчасть")

    def __str__(self):
        return f"{self.name} ({self.quantity}) В {self.warehouse.name}"
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Arrival(models.Model):
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name='arrivals'
    )
    date = models.DateField(verbose_name="Дата поступления")
    country_of_origin = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='arrival_products', 
                                          verbose_name="Страна происхождения", null=True, blank=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Arrival #{self.id} → {self.warehouse.name}"
    
    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступления"
    

class ArrivalProduct(models.Model):
    arrival = models.ForeignKey(
        Arrival, on_delete=models.PROTECT, related_name='items'
    )
    name = models.CharField(max_length=100, verbose_name="Название")
    article_number = models.CharField(max_length=50, verbose_name="Артикул")
    quantity = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    # selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена продажи", 
    #                                     null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='arrival_products', verbose_name="Бренд", 
                              null=True, blank=True)
    suits_for = models.CharField(max_length=200, verbose_name="Подходит для", null=True, blank=True,
                                 help_text="Укажите модели автомобилей, для которых подходит эта запчасть")

    def __str__(self):
        return f"{self.article_number} × {self.quantity}"
    
    class Meta:
        verbose_name = "Товар поступления"
        verbose_name_plural = "Товары поступлений"


class CurrencyRate(models.Model):
    currency_code = models.CharField(max_length=3, unique=True, verbose_name="Код валюты")
    rate_to_usd = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс к USD")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return f"{self.currency_code}: {self.rate_to_usd}"
    
    class Meta:
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"
