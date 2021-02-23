from django.urls import path

from .views import BasketView, add_to_basket, increase_or_decrease_count, delete_item, calculate_total_price, \
    create_order, PaymentView

urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket_detail'),
    path('add_to_basket/', add_to_basket, name='add_to_basket'),
    path('increase_or_decrease_count/', increase_or_decrease_count, name='increase_or_decrease_count'),
    path('delete_item/', delete_item, name='delete_item'),
    path('calculate_total_price/', calculate_total_price, name='calculate_total_price'),
    path('create_order/', create_order, name='create_order'),
    path('payment/', PaymentView.as_view(), name='payment_view'),
]
