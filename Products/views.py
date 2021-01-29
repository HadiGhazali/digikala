from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic.list import MultipleObjectMixin

from .models import Category, Product, ShopProduct


class ProductSingle(DetailView):
    model = Product
    template_name = 'product/post_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_categories'] = get_categories_of_product(self.object)
        context['shop_products'] = ShopProduct.objects.filter(product=self.object)
        context['images'] = self.object.product_image.all()[:2]
        return context


class CategoryDetailView(DetailView, MultipleObjectMixin):
    model = Category
    template_name = 'product/category_view.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = Product.objects.filter(category=self.object)
        context = super(CategoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['products'] = object_list
        return context


def get_categories_of_product(product):
    categories = []
    product_category = product.category
    categories.append(product_category)
    while product_category.parent is not None:
        categories.append(product_category)
        product_category = product_category.parent
    return categories
