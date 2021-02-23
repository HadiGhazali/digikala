from django.shortcuts import render
from django.views.generic import TemplateView

from .models import SlideShow, BrandIntroduction
from Products.models import Product, Category


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        context['slide_list'] = SlideShow.objects.all()
        context['products'] = Product.objects.all()[:10]
        context['categories'] = Category.objects.all()[:5]
        context['BrandIntroduction'] = BrandIntroduction.objects.all()[:2]
        context['CarProducts'] = Product.objects.filter(category__slug='kodakvanozad')
        context['Mavadshoyande'] = Product.objects.filter(category__slug='lebasemardane')
        return context

