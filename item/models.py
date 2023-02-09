from django.db import models


class Items(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.IntegerField()
    stripe_product_id = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f'Продукт: {self.name}'

    class Meta:
        verbose_name = 'items'
        verbose_name_plural = 'item'


class Discount(models.Model):
    item = models.ForeignKey(to=Items, on_delete=models.CASCADE)
    rebate = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'Cкидка для товара {self.item.name} | Итоговая цена {self.item.price - self.rebate}'

    class Meta:
        verbose_name = 'discounts'
        verbose_name_plural = 'discount'


class Tax(models.Model):
    item = models.ForeignKey(to=Items, on_delete=models.CASCADE)
    taxation = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'Налог на {self.item.name} - {self.taxation}'

    class Meta:
        verbose_name = 'goods tax'
        verbose_name_plural = 'tax'


class Order(models.Model):
    order_history = models.JSONField(default=dict)
    time_created = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(to=Discount, on_delete=models.CASCADE)
    tax = models.ForeignKey(to=Tax, on_delete=models.CASCADE)

    def __str__(self):
        return f'Номер заказа {self.id}'

    class Meta:
        verbose_name = 'orders'
        verbose_name_plural = 'order'
