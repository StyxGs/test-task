"""Stripe_pay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from item.views import (add_item_to_order, create_stripe_session, order,
                        order_buy, purchase_item)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<int:item_id>', create_stripe_session, name='buy'),
    path('item/<int:item_id>', purchase_item, name='item'),
    path('order/<int:item_id>', order, name='order'),
    path('order-add/<int:number_order>/<int:item_id>', add_item_to_order, name='item_add'),
    path('order-buy/<int:number_order>', order_buy, name='order_buy'),
]
