# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.views.generic.list import MultipleObjectMixin
from django.http import HttpResponse
import json
from .forms import CommentForm
from .models import Category, Product, ShopProduct, Comment


class ProductSingle(DetailView):
    model = Product
    template_name = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sub_categories = get_children_categories_of_product(self.object)
        context['related_categories'] = get_parent_categories_of_product(self.object)
        context['children_categories'] = sub_categories
        context['shop_products'] = ShopProduct.objects.filter(product=self.object)
        context['images'] = self.object.product_image.all()[:3]
        related_product = Product.objects.filter(category=self.object.category)
        if len(related_product) < 12:
            related_product |= Product.objects.filter(category__in=sub_categories)[:12 - len(related_product)]
        related_product = related_product.exclude(slug=self.object.slug)
        context['related_products'] = related_product
        comment_form = CommentForm()
        context['form'] = comment_form
        context['comments'] = self.object.product_comment.all()[::-1][:9]
        return context


class CategoryDetailView(DetailView, MultipleObjectMixin):
    model = Category
    template_name = 'product/category_view.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = Product.objects.filter(category=self.object).order_by('create_at')
        context = super(CategoryDetailView, self).get_context_data(object_list=object_list, **kwargs)

        sub_categories = get_sub_categories_of_category(self.object)
        parent_categories = get_parent_categories_of_category(self.object)
        context['products'] = object_list
        context['sub_categories'] = sub_categories
        context['parent_categories'] = parent_categories
        return context


def get_parent_categories_of_product(product):
    parent_categories = []
    product_category = product.category
    parent_categories.append(product_category)
    while product_category.parent is not None:
        product_category = product_category.parent
        parent_categories.append(product_category)
    return parent_categories


def get_children_categories_of_product(product):
    product_category = product.category
    sub_categories = []
    for sub_category in product_category.children.all():
        sub_categories.append(sub_category)
    return sub_categories


def get_sub_categories_of_category(category):
    sub_categories = []
    for sub_category in category.children.all():
        sub_categories.append(sub_category)
    return sub_categories


def get_parent_categories_of_category(category):
    parent_categories = []
    while category.parent is not None:
        category = category.parent
        parent_categories.append(category)
    return parent_categories


@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    user = request.user
    new_comment = Comment.objects.create(user=user, product_id=data['product_id'], text=data['text'],
                                         rate=data['rate'])
    response = {'product_id': new_comment.id, 'text': new_comment.text, 'rate': new_comment.rate}
    return HttpResponse(json.dumps(response), status=201)

