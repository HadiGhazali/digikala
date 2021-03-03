import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from Accounts.forms import LoginForm, UserRegistrationForm, AddAddressForm, EditProfile, ApplyingForShopForm, \
    EditShopProduct, AddShopProductForm
from Accounts.models import Address, Shop
from Products.models import ShopProduct, Product


class Login(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


class Logout(LogoutView):
    pass


class RegisterView(FormView):
    form_class = UserRegistrationForm
    success_url = '../login'
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        user = form.save(commit=False)
        password = user.password
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(LoginRequiredMixin, TemplateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/profile.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        address_form = AddAddressForm()
        context['address_form'] = address_form

        return context


@csrf_exempt
def add_address(request):
    if request.method == 'POST':
        data = request.POST
        user = request.user
        new_address = Address.objects.create(city=data.get('city'), street=data.get('street'),
                                             zip_code=data.get('zip_code'),
                                             allay=data.get('allay'), user=user)

        response = {'address': new_address.show_address}
        return HttpResponse(json.dumps(response), status=201)
    return HttpResponse(status=400)


class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditProfile
    success_url = '../home'
    template_name = 'accounts/editProfile.html'
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        user = form.save(commit=False)
        password = user.password
        user.set_password(password)
        user.save()
        update_session_auth_hash(self.request, self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class ApplyingForShopView(LoginRequiredMixin, FormView):
    form_class = ApplyingForShopForm
    template_name = 'accounts/applying_for_shop.html'
    success_url = reverse_lazy('home_view')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.save()
        return HttpResponseRedirect(self.get_success_url())


class UserShop(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'accounts/user_shops.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset


class ShopView(ListView):
    model = Shop
    template_name = 'accounts/all_shop.html'


class ShopProductView(LoginRequiredMixin, DetailView):
    model = Shop
    template_name = 'accounts/shop_product.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        if self.request.user == self.object.user:
            object_list = ShopProduct.objects.filter(shop=self.object)
            context = super(ShopProductView, self).get_context_data(object_list=object_list, **kwargs)
            context['result'] = 'true'
            return context
        else:
            context = super(ShopProductView, self).get_context_data()
            context['result'] = None
            return context


class ShopProductEdit(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/shop_product_edit.html'
    form_class = EditShopProduct
    success_url = reverse_lazy('user_shop')
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        shop_slug = self.kwargs.get("shop_slug")
        product_slug = self.kwargs.get("product_slug")
        my_object = ShopProduct.objects.get(shop__slug=shop_slug, product__slug=product_slug)
        return my_object

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if form:
            form.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        shop_slug = self.kwargs.get("shop_slug")
        if self.request.user == Shop.objects.get(slug=shop_slug).user:
            context = super(ShopProductEdit, self).get_context_data()
            return context
        else:
            context = super(ShopProductEdit, self).get_context_data()
            context['form'] = None
            return context


class ShopProductAdd(LoginRequiredMixin, FormView):
    template_name = 'accounts/shop_product_add_product.html'
    form_class = AddShopProductForm
    success_url = reverse_lazy('user_shop')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        shop_slug = self.kwargs.get('shop_slug')
        my_form = form.save(commit=False)
        my_form.shop = Shop.objects.get(slug=shop_slug)
        my_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        shop_slug = self.kwargs.get('shop_slug')
        if self.request.user == Shop.objects.get(slug=shop_slug).user:
            context = super(ShopProductAdd, self).get_context_data()
            context['shop'] = Shop.objects.get(slug=shop_slug)
            return context
        else:
            context = super(ShopProductAdd, self).get_context_data()
            context['form'] = None
            context['shop'] = Shop.objects.get(slug=shop_slug)
            return context
