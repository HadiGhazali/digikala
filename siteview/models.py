from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from Products.models import Product, Category


class SlideShow(models.Model):
    title = models.CharField(_('Title'), max_length=250)
    subtitle = models.CharField(_('Sub title'), max_length=250)
    image = models.ImageField(_('Background image'), upload_to='siteview/slide_show/images')
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)
    action_text = models.CharField(_('Action text'), max_length=50)
    action_url = models.URLField(_('Action url'))

    def __str__(self):
        return self.title


class BrandIntroduction(models.Model):
    Brand = models.CharField(_('Title'), max_length=250)
    image = models.ImageField(_('Background image'), upload_to='siteview/slide_show/images')
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    update_at = models.DateTimeField(_('Update at'), auto_now=True)
    action_url = models.URLField(_('Action url'))

    def __str__(self):
        return self.Brand


class Special(models.Model):
    product = models.OneToOneField(Product, verbose_name=_('Product'), on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class SpecialCategory(models.Model):
    category = models.OneToOneField(Category, verbose_name=_('Category'), on_delete=models.CASCADE)

    def __str__(self):
        return self.category.title
