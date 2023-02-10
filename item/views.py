import stripe
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


from item.models import Discount, Items, Order, Tax

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(request, item_id):
    product = Items.objects.get(id=item_id)
    checkout_session = product.create_stripe_session()
    return JsonResponse({'session_id': checkout_session.id})


def purchase_item(request, item_id):
    product = Items.objects.get(id=item_id)
    checkout_session = product.create_stripe_session()
    if request.method == 'POST':
        return HttpResponseRedirect(checkout_session.url, status=303)
    context = {'title': f'Buy - {product.name}',
               'name': product.name,
               'description': product.description,
               'price': product.price,
               'item_id': item_id,
               'session_id': checkout_session.id}
    return render(request, 'item/purchase.html', context)


def order(request, item_id):
    discount = Discount.objects.get(item_id=item_id)
    tax = Tax.objects.get(item_id=item_id)
    Order.objects.create(item_id=item_id, discount=discount, tax=tax,
                         number_order=Order.objects.all().count() + 1, quantity=1)
    return HttpResponse('Ваш заказ создан, товар добавлен к заказу')


def add_item_to_order(request, number_order, item_id):
    Order.add_item(number_order, item_id)
    return HttpResponse('Товар добавлен к выбранному заказу')


def order_buy(request, number_order):
    checkout_session = stripe.checkout.Session.create(
        line_items=Order.order_buy(number_order),
        mode="payment",
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/cancel',
    )
    return HttpResponseRedirect(checkout_session.url, status=303)
