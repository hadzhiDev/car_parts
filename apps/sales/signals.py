from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import transaction

from .models import SaleItem, Payment


@receiver(pre_save, sender=SaleItem)
def saleitem_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_quantity = 0
        instance._old_price = 0
        return

    old = SaleItem.objects.get(pk=instance.pk)
    instance._old_quantity = old.quantity
    instance._old_price = old.sale_price


@receiver(post_save, sender=SaleItem)
@transaction.atomic
def saleitem_post_save(sender, instance, created, **kwargs):
    product = instance.product
    client = instance.sale.client

    quantity_delta = instance.quantity - instance._old_quantity
    price_delta = (instance.quantity * instance.sale_price) - (
        instance._old_quantity * instance._old_price
    )

    product.quantity -= quantity_delta
    if product.quantity < 0:
        product.quantity = 0
    product.save()

    client.balance += price_delta
    client.save()



@receiver(post_delete, sender=SaleItem)
def saleitem_post_delete(sender, instance, **kwargs):
    product = instance.product
    client = instance.sale.client

    product.quantity += instance.quantity
    product.save()

    client.balance -= instance.quantity * instance.sale_price
    client.save()


@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    client = instance.client
    client.balance -= instance.amount
    client.save()


@receiver(post_delete, sender=Payment)
def payment_post_delete(sender, instance, **kwargs):
    client = instance.client
    client.balance += instance.amount
    client.save()
