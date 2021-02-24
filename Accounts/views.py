import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView
from Accounts.forms import LoginForm, UserRegistrationForm, AddAddressForm, EditProfile, ApplyingForShopForm
from Accounts.models import Address


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


class ProfileView(TemplateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/profile.html'

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


class EditProfileView(UpdateView):
    form_class = EditProfile
    success_url = '../home'
    template_name = 'accounts/editProfile.html'

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


class ApplyingForShopView(FormView):
    form_class = ApplyingForShopForm
    template_name = 'accounts/applying_for_shop.html'
    success_url = reverse_lazy('home_view')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.save()
        return HttpResponseRedirect(self.get_success_url())
