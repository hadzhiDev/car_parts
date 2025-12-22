from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import Product, ArrivalProduct


def normalize_name(name: str) -> str:
    if not name:
        return ''
    return ' '.join(name.strip().upper().split())


@receiver(pre_save, sender=ArrivalProduct)
def arrivalproduct_pre_save(sender, instance, **kwargs):
    instance.name = normalize_name(instance.name)

    if not instance.pk:
        instance._old_quantity = 0
        return

    old = ArrivalProduct.objects.get(pk=instance.pk)
    instance._old_quantity = old.quantity


@receiver(post_save, sender=ArrivalProduct)
def arrivalproduct_post_save(sender, instance, created, **kwargs):
    product = Product.objects.filter(
        warehouse=instance.arrival.warehouse,
        article_number=instance.article_number,
        brand=instance.brand,
        country_of_origin=instance.arrival.country_of_origin,
        name=instance.name,
    ).first()

    if not product:
        product = Product.objects.create(
            warehouse=instance.arrival.warehouse,
            name=instance.name,
            article_number=instance.article_number,
            brand=instance.brand,
            country_of_origin=instance.arrival.country_of_origin,
            quantity=0,
            cost_price=instance.cost_price,
            suits_for=instance.suits_for,
        )

    delta = instance.quantity if created else instance.quantity - instance._old_quantity

    product.quantity = max(0, product.quantity + delta)
    product.cost_price = instance.cost_price
    product.save()



@receiver(post_delete, sender=ArrivalProduct)
def arrivalproduct_post_delete(sender, instance, **kwargs):
    try:
        product = Product.objects.get(
            warehouse=instance.arrival.warehouse,
            name=instance.name,  
            brand=instance.brand,
            country_of_origin=instance.arrival.country_of_origin,
        )
        product.quantity = max(0, product.quantity - instance.quantity)
        product.save()
    except Product.DoesNotExist:
        pass
