from django.contrib import admin

from item.models import Discount, Items, Order, Tax


class DiscountsAdmin(admin.TabularInline):
    model = Discount
    fields = ('discount',)
    extra = 0


class TaxAdmin(admin.TabularInline):
    model = Tax
    fields = ('taxation',)
    extra = 0


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    ordering = ('price',)
    inlines = (DiscountsAdmin, TaxAdmin)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('discount', 'tax')
