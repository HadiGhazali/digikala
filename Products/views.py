from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from .models import Category


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'product/category_view.html'

