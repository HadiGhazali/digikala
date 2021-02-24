from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from Accounts.models import User, Email, Shop, Address, ApplyingForShop


# Register your models here.

class AddressAdminInline(admin.TabularInline):
    model = Address
    fields = (
        'city', 'street', 'zip_code', 'allay'
    )

    extra = 1
    show_change_link = True


class UserAdmin(BaseUserAdmin):
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'image', 'phone_number')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'phone_number', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    inlines = [
        AddressAdminInline
    ]


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('to', 'subject')
    search_fields = ('subject',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(ApplyingForShop)
