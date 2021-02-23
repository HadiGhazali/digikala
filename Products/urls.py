from django.urls import path

from .views import CategoryDetailView, ProductSingle, create_comment

urlpatterns = [
    path('search/<slug:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>', ProductSingle.as_view(), name='product_single'),
    path('create_comment/', create_comment, name='create_comment'),
]
