from django.urls import path

from .views import CategoryDetailView, ProductSingle

urlpatterns = [
    path('search/<slug:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>', ProductSingle.as_view(), name='category_detail')
]
