from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from Products.models import ShopProduct

# Create your models here.
User = get_user_model()


class Basket(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), on_delete=models.CASCADE,
                                related_query_name='user_baskets',
                                related_name='user_baskets')
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')

    @property
    def total_price(self):
        t_price = 0
        item_list = self.get_item()
        for item in item_list:
            t_price += item.total_price_of_one_item
        return t_price

    def get_item(self):
        item_list = self.basket_item.all()
        return item_list

    @property
    def show_item(self):
        items = ''
        for item in self.get_item():
            items += item.__str__()
        return items

    @property
    def count_of_items(self):
        n = 0
        for i in self.get_item():
            n += i.count
        return n


class BasketItem(models.Model):
    shop_product = models.ForeignKey(ShopProduct, verbose_name=_('Shop product'), on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, verbose_name=_('Basket'), on_delete=models.CASCADE, related_name='basket_item',
                               related_query_name='basket_item')
    count = models.PositiveIntegerField(_('Count'))
    price = models.PositiveIntegerField(_('Price'))

    class Meta:
        unique_together = [['shop_product', 'basket']]

    def set_price(self):
        self.price = self.shop_product.price
        self.save()

    def add_count(self):
        self.count += 1
        self.save()

    def decrease_count(self):
        self.count -= 1
        self.save()

    @property
    def total_price_of_one_item(self):
        return self.price * self.count

    @property
    def get_name(self):
        return self.shop_product.product.name

    @property
    def get_shop_name(self):
        return self.shop_product.shop.name

    def __str__(self):
        string = '{} in {}'.format(self.get_name, self.get_shop_name)
        return string


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='user_order',
                             related_query_name='user_order')
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)

    description = models.TextField(_('Description'), null=True, blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @property
    def total_price(self):
        t_price = 0
        item_list = self.get_item()
        for item in item_list:
            t_price += item.total_price_of_one_item
        return t_price

    def get_item(self):
        return self.order_item.all()

    @property
    def show_item(self):
        items = ''
        for item in self.get_item():
            items += item.__str__()
        return items

    @property
    def count_of_items(self):
        n = 0
        for i in self.get_item():
            n += i.count
        return n


class OrderItem(models.Model):
    shop_product = models.ForeignKey(ShopProduct, verbose_name=_('Order Item'), on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.CASCADE, related_name='order_item',
                              related_query_name='order_item')
    count = models.PositiveIntegerField(_('Count'))
    price = models.PositiveIntegerField(_('Price'))

    @property
    def total_price_of_one_item(self):
        return self.price * self.count

    @property
    def get_name(self):
        return self.shop_product.product.name

    @property
    def get_shop_name(self):
        return self.shop_product.shop.name

    def __str__(self):
        string = '{} in {}'.format(self.get_name, self.get_shop_name)
        return string


class Payment(models.Model):
    order = models.OneToOneField(Order, verbose_name=_('order'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(_('amount'))

    def set_amount(self):
        self.amount = self.order.total_price
        self.save()

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
