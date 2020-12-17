from django.contrib.auth import get_user_model
from django.db import models
from Accounts.models import Shop
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_lazy

User = get_user_model()


class Category(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', related_query_name='children')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    details = models.TextField(_('Details'))
    image = models.ImageField(_('image'), upload_to='product/brand/image', null=True, blank=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name


class Product(models.Model):
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=50)
    image = models.ImageField(_('image'), upload_to='product/product/mainImage', null=True, blank=True)
    details = models.TextField(_('Details'))

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(_('image'), upload_to='product/product/otherImage', null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE)


class ProductMeta(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE)
    value = models.TextField(_('Value'))
    label = models.CharField(_('Label'), max_length=150)


class Comment(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL, null=True)
    text = models.TextField(_('Text'))
    rate = models.IntegerField(_('Rate'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class ShopProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name=_('shop'), on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'))
    price = models.IntegerField(_('Price'))


class Off(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE)
    percentage = models.FloatField(_('Percentage'))
    code = models.CharField(_('Code'), max_length=150)
