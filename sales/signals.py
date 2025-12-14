# @receiver(post_save, sender=Sale)
# def update_product_quantity_on_sale(sender, instance, created, **kwargs):
#     if created:
#         for item in instance.items.all():
#             product = item.product
#             product.quantity -= item.quantity_sold
#             product.save()
#         print("Product quantities updated after sale.")
#         client = instance.client
#         total_sale_amount = sum(item.sale_price * item.quantity_sold for item in instance.items.all())
#         client.balance -= total_sale_amount
#         client.save()