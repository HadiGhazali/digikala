from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from Accounts.models import Shop
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class Category(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', related_query_name='children')
    image = models.ImageField(upload_to='product/category/image', null=True, blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


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
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='brand_product', related_query_name='brand_product')
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='category_product', related_query_name='category_product')
    name = models.CharField(_('Name'), max_length=50)
    image = models.ImageField(_('image'), upload_to='product/product/mainImage', null=True, blank=True)
    details = models.TextField(_('Details'))
    review = models.TextField(_('Review'), null=True, blank=True)
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.name

    @property
    def like_count(self):
        q = self.product_like.filter(condition=True)
        return q.count()

    @property
    def dislike_count(self):
        q = self.product_like.filter(condition=False)
        return q.count()

    @property
    def calculate_price(self):
        shop = self.shop_product_product.order_by('price')[0]
        return shop.price


class ProductImage(models.Model):
    image = models.ImageField(_('image'), upload_to='product/product/otherImage', null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE,
                                related_name='product_image', related_query_name='product_image')


class ProductMeta(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE,
                                related_query_name='product_meta', related_name='product_meta')
    value = models.TextField(_('Value'))
    label = models.CharField(_('Label'), max_length=150)


class Comment(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE,
                                related_name='product_comment', related_query_name='product_comment')
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.SET_NULL, null=True)
    text = models.TextField(_('Text'))
    rate = models.IntegerField(_('Rate'))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class ShopProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE,
                                related_name='shop_product_product', related_query_name='shop_product_product')
    shop = models.ForeignKey(Shop, verbose_name=_('shop'), on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'))
    price = models.IntegerField(_('Price'))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        unique_together = [['product', 'shop']]
        verbose_name = _("Shop Products")
        verbose_name_plural = _("Shop Products")

    @property
    def check_status(self):
        if self.quantity >= 0:
            return True
        else:
            return False

    def __str__(self):
        return '{} in {}'.format(self.product.name, self.shop.name)


class Like(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE,
                                related_name='product_like', related_query_name='product_like')
    condition = models.BooleanField('Condition')
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)


class UrlHit(models.Model):
    product = models.OneToOneField(Product, verbose_name=_('product'), on_delete=models.CASCADE, related_name='url_hit',
                                   related_query_name='url_hit')
    url = models.CharField(max_length=150, unique=True)
    hits = models.PositiveIntegerField(default=0)
    daily_hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.url)

    def increase(self):
        self.hits += 1
        self.save()

    def get_daily_hits(self):
        return self.daily_hits

    def set_daily_hits(self, daily_hits):
        self.daily_hits = daily_hits
        self.save()


class HitCount(models.Model):
    url_hit = models.ForeignKey(UrlHit, editable=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(null=True)

    def updating_date(self):
        self.update_date = timezone.now()
        self.save()

    def get_date(self):
        return self.update_date.date()

    def set_user(self, user):
        self.user = user
        self.save()


class UserFavoriteProduct(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE,
                             related_name='user_favorite_product_user', related_query_name='user_favorite_product_user')
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE,
                                related_name='user_favorite_product_product',
                                related_query_name='user_favorite_product_product')

    class Meta:
        unique_together = [['product', 'user']]
