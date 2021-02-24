from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from Accounts.models import Address, ApplyingForShop
from Accounts.validators import validate_username, validate_phone_number, validate_password

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Email'), max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True)


class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'phone_number', 'first_name', 'last_name', 'image')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        if password != password2:
            raise ValidationError(
                _("password don't match"),
                code='invalid'
            )
        validate_phone_number(self.cleaned_data['phone_number'])

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        validate_username(username)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        validate_password(password)
        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number[0:3] == '098':
            phone_number = '09' + phone_number.split('098')[1]
        if phone_number[0:3] == '+98':
            phone_number = '09' + phone_number.split('+98')[1]
        return phone_number


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('city', 'street', 'zip_code', 'allay')
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'address-city'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'id': 'address-street'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'id': 'address-zip_code'}),
            'allay': forms.TextInput(attrs={'class': 'form-control', 'id': 'address-allay'}),
        }


class EditProfile(forms.ModelForm):
    password2 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'phone_number', 'first_name', 'last_name', 'image')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        if password != password2:
            raise ValidationError(
                _("password don't match"),
                code='invalid'
            )
        validate_phone_number(self.cleaned_data['phone_number'])


class ApplyingForShopForm(forms.ModelForm):
    class Meta:
        model = ApplyingForShop
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
