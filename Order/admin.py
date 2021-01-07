from django.contrib import admin

# Register your models here.
from Order.models import Basket, Order, OrderItem, BasketItem, Payment


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price')
    readonly_fields = ('show_item', )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('shop_product', 'price')


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('shop_product', 'price')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'user')
