from django.urls import path, re_path

from Accounts.views import Login, Logout, RegisterView, ProfileView, add_address, EditProfileView, UserShop, ShopView, \
    ShopProductView, ShopProductEdit, ShopProductAdd
from Products.views import AddProductView

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('add_address/', add_address, name='add_address'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('user_shop/', UserShop.as_view(), name='user_shop'),
    path('user_shop/<slug:slug>/', ShopProductView.as_view(), name='shop_product_view'),
    path('user_shop/<slug:shop_slug>/add_product/', ShopProductAdd.as_view(), name='shop_product_add_product'),

    path('user_shop/<slug:shop_slug>/<slug:product_slug>/', ShopProductEdit.as_view(), name='shop_product_view_detail'),
    path('all_shop/', ShopView.as_view(), name='all_shop'),
]
