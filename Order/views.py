from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import json

from Products.models import ShopProduct
from .models import Basket, BasketItem, Order, OrderItem, Payment


# Create your views here.
class BasketView(TemplateView):
    template_name = 'order/basket.html'

    def get_context_data(self, **kwargs):
        context = super(BasketView, self).get_context_data()
        Basket.objects.get_or_create(user=self.request.user)
        basket = Basket.objects.get(user=self.request.user)
        context['basket'] = basket
        context['basket_item'] = basket.get_item()
        return context


def get_slug(request):
    path_url = request.path
    slug = str(path_url).split('/')[2]
    return slug


@csrf_exempt
def add_to_basket(request):
    data = json.loads(request.body)
    shop_product = get_object_or_404(ShopProduct, id=data['shop_product_id'])
    basket = request.user.user_baskets
    new_basket_item = BasketItem.objects.create(shop_product=shop_product, count=1, price=0, basket=basket)

    new_basket_item.set_price()
    return HttpResponse(status=201)


@csrf_exempt
def increase_or_decrease_count(request):
    data = json.loads(request.body)
    item = get_object_or_404(BasketItem, id=data['item_id'])
    if data['condition'] and item.count <= item.shop_product.quantity:
        item.add_count()
    elif not data['condition']:
        item.decrease_count()
    if item.count == 0:
        response = {'item_count': item.count, 'item_id': item.id, 'delete_status': 0,
                    'total_price': item.total_price_of_one_item}
        item.delete()
    else:
        response = {'item_count': item.count, 'item_id': item.id, 'delete_status': 1,
                    'total_price': item.total_price_of_one_item}
    return HttpResponse(json.dumps(response), status=201)


@csrf_exempt
def delete_item(request):
    data = json.loads(request.body)
    item = get_object_or_404(BasketItem, id=data['item_id'])
    response = {'item_id': item.id}
    item.delete()
    return HttpResponse(json.dumps(response), status=201)


@csrf_exempt
def calculate_total_price(request):
    data = json.loads(request.body)
    basket = get_object_or_404(Basket, id=data['basket_id'])
    total_price = basket.total_price
    response = {'total_price': total_price, 'count_of_items': basket.count_of_items}
    return HttpResponse(json.dumps(response), status=201)


@csrf_exempt
def create_order(request):
    data = json.loads(request.body)
    basket = get_object_or_404(Basket, id=data['basket_id'])
    new_order = Order.objects.create(user=basket.user, description=data['description'])

    for basket_item in basket.basket_item.all():
        OrderItem.objects.create(order=new_order, shop_product=basket_item.shop_product,
                                 count=basket_item.count, price=basket_item.price)

    payment, payment_created = Payment.objects.get_or_create(order=new_order, user=request.user, amount=0)

    if payment_created:
        payment.set_amount()

    for basket_item in basket.basket_item.all():
        basket_item.delete()

    return HttpResponse(status=201)


class PaymentView(TemplateView):
    template_name = 'order/payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data()
        basket = self.request.user.user_baskets
        context['basket'] = basket
        context['basket_item'] = basket.get_item()
        return context


@csrf_exempt
def get_count_of_basket_item(request):
    basket = get_object_or_404(Basket, user=request.user)
    response = {'count_of_items': basket.count_of_items}
    return HttpResponse(json.dumps(response), status=201)
