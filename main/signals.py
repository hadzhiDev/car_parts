from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import Product, ArrivalProduct


@receiver(pre_save, sender=ArrivalProduct)
def arrivalproduct_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        # New object → handled in post_save
        instance._old_quantity = 0
        return

    old = ArrivalProduct.objects.get(pk=instance.pk)
    instance._old_quantity = old.quantity


@receiver(post_save, sender=ArrivalProduct)
def arrivalproduct_post_save(sender, instance, created, **kwargs):
    product, created_product = Product.objects.get_or_create(
        article_number=instance.article_number,
        warehouse=instance.arrival.warehouse,

        defaults={
            'name': instance.name,
            'quantity': 0,
            'cost_price': instance.cost_price,
            # 'selling_price': instance.selling_price,
            'brand': instance.brand,
            'country_of_origin': instance.arrival.country_of_origin,
            'suits_for': instance.suits_for,
        }
    )

    if created:
        delta = instance.quantity
    else:
        delta = instance.quantity - instance._old_quantity

    product.quantity += delta
    product.cost_price = instance.cost_price
    # product.selling_price = instance.selling_price
    product.save()


@receiver(post_delete, sender=ArrivalProduct)
def arrivalproduct_post_delete(sender, instance, **kwargs):
    try:
        product = Product.objects.get(
            article_number=instance.article_number,
            warehouse=instance.arrival.warehouse
        )
        product.quantity -= instance.quantity 

        if product.quantity < 0:
            product.quantity = 0

        product.save()
    except Product.DoesNotExist:
        pass
        