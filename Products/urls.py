from django.urls import path

from Accounts.views import ApplyingForShopView
from .views import CategoryDetailView, ProductSingle, create_comment, get_category, ShopDetailView, SearchView, \
    add_to_favorite, FavoriteView

urlpatterns = [
    path('searching/', SearchView.as_view(), name='search_detail'),
    path('search/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductSingle.as_view(), name='product_single'),
    path('create_comment/', create_comment, name='create_comment'),
    path('get_category/', get_category, name='get_category'),
    path('applying_for_shop/', ApplyingForShopView.as_view(), name='applying_for_shop'),
    path('shop/<slug:slug>/', ShopDetailView.as_view(), name='shop_detail'),
    path('add_to_favorite/', add_to_favorite, name='add_to_favorite'),
    path('favorite_page/', FavoriteView.as_view(), name='favorite_page'),
]
