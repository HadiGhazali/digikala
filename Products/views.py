# Create your views here.
from datetime import timedelta
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, FormView
from django.views.generic.list import MultipleObjectMixin, ListView
from django.http import HttpResponse, HttpResponseRedirect
import json

from Accounts.models import Shop
from .forms import CommentForm, AddProductForm
from .models import Category, Product, ShopProduct, Comment, HitCount, UrlHit, Brand, UserFavoriteProduct
from django.utils import timezone


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
        hit = hit_count(self.request, UrlHit)
        daily_hit = calculate_daily_hit(self.request)
        comment_form = CommentForm()
        context['form'] = comment_form
        context['comments'] = self.object.product_comment.all()[::-1][:9]
        return context


class CategoryDetailView(DetailView, MultipleObjectMixin):
    model = Category
    template_name = 'product/category_view.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        brands = self.request.GET.getlist('brand', None)
        order_by = self.request.GET.get('order_by', None)
        if brands:
            object_list = Product.objects.filter(category=self.object, brand__slug__in=brands).order_by('create_at')
        else:
            object_list = Product.objects.filter(category=self.object).order_by('create_at')
        if order_by == 'create_at':
            object_list = object_list.order_by('create_at')
        elif order_by == 'low_price':
            object_list = sorted(object_list, key=lambda t: t.calculate_price)
        elif order_by == 'high_price':
            object_list = sorted(object_list, key=lambda t: t.calculate_price)[::-1]
        elif order_by == 'hit_count':
            object_list = object_list.order_by('url_hit__hits')

        brand_list = set()
        context = super(CategoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['category_id'] = self.object.id
        for product in Product.objects.filter(category=self.object):
            if product.brand is not None:
                brand_list.add(product.brand)
        context['brands'] = brand_list
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


def updating_date_of_obj(url, ip, s_key):
    HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
    obj = HitCount.objects.get(url_hit=url, ip=ip, session=s_key)
    obj.updating_date()


@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    user = request.user
    new_comment = Comment.objects.create(user=user, product_id=data['product_id'], text=data['text'],
                                         rate=data['rate'])
    response = {'product_id': new_comment.id, 'text': new_comment.text, 'rate': new_comment.rate}
    return HttpResponse(json.dumps(response), status=201)


@csrf_exempt
def get_category(request):
    result = {}
    main_categories = Category.objects.filter(parent=None)
    i = 0
    for main_category in main_categories:
        sub_category_slugs = []
        sub_category_titles = []
        for sub_category in main_category.children.all():
            sub_category_slugs.append(sub_category.slug)
            sub_category_titles.append(sub_category.title)

        result[i] = {'slug': main_category.slug, 'title': main_category.title,
                     'sub_categories': {'slugs': sub_category_slugs, 'titles': sub_category_titles}}
        i += 1
    return HttpResponse(json.dumps(result), status=201)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_product_slug(request):
    path_url = request.path
    product_slug = str(path_url)
    product_slug = product_slug.split('/')
    product_slug = product_slug[2]
    return product_slug


def hit_count(request, obj):
    if not request.session.session_key:
        request.session.save()
    s_key = request.session.session_key
    ip = get_client_ip(request)
    path_url = request.path
    product_slug = get_product_slug(request)
    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        return 'Product does not exits'
    url, url_created = obj.objects.get_or_create(url=path_url, product=product)
    if url_created or (ip and request.path not in request.session):
        if request.user.id:
            track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key, user=request.user)
        else:
            track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
        if created:
            url.increase()
            request.session[ip] = ip
            request.session[request.path] = request.path
    updating_date_of_obj(url, ip, s_key)
    return url.hits


def get_day():
    return timezone.now()


def calculate_daily_hit(request):
    slug = get_product_slug(request)
    today = get_day()
    object_hit_daily = HitCount.objects.filter(update_date__gte=today - timedelta(days=1),
                                               url_hit__product__slug=slug).count()
    url_hit_obj = UrlHit.objects.get(url=request.path)
    url_hit_obj.set_daily_hits(object_hit_daily)
    return object_hit_daily


class ShopDetailView(DetailView, MultipleObjectMixin):
    model = Shop
    template_name = 'accounts/shop.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        brands = self.request.GET.getlist('brand', None)
        order_by = self.request.GET.get('order_by', None)
        shop_products = ShopProduct.objects.filter(shop=self.object)
        object_list = Product.objects.filter(shop_product_product__in=shop_products).order_by('create_at')

        if brands:
            object_list = object_list.filter(brand__slug__in=brands).order_by('create_at')

        if order_by == 'create_at':
            object_list = object_list.order_by('create_at')
        elif order_by == 'low_price':
            object_list = sorted(object_list, key=lambda t: t.calculate_price)
        elif order_by == 'hit_count':
            object_list = object_list.order_by('url_hit__hits')
        elif order_by == 'high_price':
            object_list = sorted(object_list, key=lambda t: t.calculate_price)[::-1]

        brand_list = set()
        context = super(ShopDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['shop_id'] = self.object.id
        for product in Product.objects.filter(shop_product_product__in=shop_products):
            if product.brand is not None:
                brand_list.add(product.brand)
        context['brands'] = brand_list
        context['products'] = object_list
        return context


class AddProductView(FormView):
    form_class = AddProductForm
    success_url = reverse_lazy('profile')
    template_name = 'product/add_product.html'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        product = form.save(commit=False)
        product.save()
        return HttpResponseRedirect(self.get_success_url())


class SearchView(ListView):
    model = Product
    template_name = 'product/search_view.html'
    paginate_by = 12

    def get_queryset(self):
        field = self.request.GET.get('search')
        if self.request.GET.get('search'):
            query_set = Product.objects.filter(
                Q(name=field) | Q(slug=field) | Q(category__title=field) | Q(category__slug=field) | Q(
                    brand__slug=field) | Q(brand__name=field))
            if query_set is None:
                query_set = Product.objects.all()
            return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        brands = self.request.GET.getlist('brand', None)
        order_by = self.request.GET.get('order_by', None)
        if brands:
            object_list = self.object_list.filter(brand__slug__in=brands).order_by('create_at')
        else:
            object_list = self.object_list.order_by('create_at')
        if order_by == 'create_at':
            object_list = object_list.order_by('create_at')
        elif order_by == 'low_price':
            object_list = sorted(object_list, key=lambda t: t.calculate_price)
        elif order_by == 'high_price':
            object_list = sorted(object_list, key=lambda t: t.calculate_price)[::-1]
        elif order_by == 'hit_count':
            object_list = object_list.order_by('url_hit__hits')
        brand_list = set()
        context = super(SearchView, self).get_context_data(object_list=object_list, **kwargs)
        for product in self.object_list:
            if product.brand is not None:
                brand_list.add(product.brand)
        context['brands'] = brand_list
        context['products'] = object_list
        return context


@csrf_exempt
def add_to_favorite(request):
    data = json.loads(request.body)
    user = request.user
    UserFavoriteProduct.objects.create(user=user, product_id=data['product_id'])
    return HttpResponse(status=201)


class FavoriteView(ListView):
    model = Product
    paginate_by = 12
    template_name = 'product/favorite_page.html'

    def get_queryset(self):
        user_favorite = UserFavoriteProduct.objects.filter(user=self.request.user)
        return Product.objects.filter(user_favorite_product_product__in=user_favorite)
