import stripe
from django.conf import settings
from django.db import models

stripe.api_key = settings.STRIPE_SECRET_KEY


class Items(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return f'Продукт: {self.name}'

    class Meta:
        verbose_name = 'items'
        verbose_name_plural = 'item'

    def create_stripe_session(self):
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "rub",
                        "product_data": {"name": self.name, "description": self.description},
                        "unit_amount": self.price * 100,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url='http://127.0.0.1:8000/success',
            cancel_url='http://127.0.0.1:8000/cancel',
        )
        return checkout_session


class Discount(models.Model):
    item = models.ForeignKey(to=Items, on_delete=models.CASCADE)
    discount = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'Скидка: {self.discount} руб.'

    class Meta:
        verbose_name = 'discounts'
        verbose_name_plural = 'discount'


class Tax(models.Model):
    item = models.ForeignKey(to=Items, on_delete=models.CASCADE)
    taxation = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'Налог: {self.taxation} руб.'

    class Meta:
        verbose_name = 'goods tax'
        verbose_name_plural = 'tax'


class Order(models.Model):
    item = models.ForeignKey(to=Items, on_delete=models.CASCADE)
    number_order = models.PositiveSmallIntegerField(default=1)
    discount = models.ForeignKey(to=Discount, on_delete=models.CASCADE)
    tax = models.ForeignKey(to=Tax, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'Заказ {self.id}'

    class Meta:
        verbose_name = 'orders'
        verbose_name_plural = 'order'

    @classmethod
    def add_item(cls, number_order, item_id):
        discount = Discount.objects.get(item_id=item_id)
        tax = Tax.objects.get(item_id=item_id)
        orders = Order.objects.filter(number_order=number_order, item_id=item_id)
        if orders:
            order = orders.first()
            order.quantity += 1
            order.save()
        else:
            Order.objects.create(number_order=number_order, item_id=item_id,
                                 discount=discount, tax=tax, quantity=1)

    @classmethod
    def order_buy(cls, number_order):
        goods = Order.objects.filter(number_order=number_order)
        line_items = []
        for product in goods:
            item = {
                "price_data": {
                    "currency": "rub",
                    "product_data": {"name": product.item.name, "description": f'Скидка: {product.discount} Налог: {product.tax}'},
                    "unit_amount": product.item.price * 100,
                },
                "quantity": product.quantity,
            }
            line_items.append(item)

        return line_items
