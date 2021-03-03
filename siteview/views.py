from django.shortcuts import render
from django.views.generic import TemplateView

from .models import SlideShow, BrandIntroduction, Special, SpecialCategory
from Products.models import Product, Category


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        slide_list = SlideShow.objects.all()
        context['slide_list'] = slide_list
        number = slide_list.count()
        number_list = []
        for i in range(1, number):
            number_list.append(i)
        context['number_list'] = number_list
        special = Special.objects.all()
        context['special_product_1'] = Product.objects.filter(special__in=special)[:8]
        context['special_product_2'] = Special.objects.all()[8:16]
        context['categories'] = Category.objects.all()[:5]
        context['BrandIntroduction'] = BrandIntroduction.objects.all()[:2]
        category_1 = SpecialCategory.objects.all()[0].category
        category_2 = SpecialCategory.objects.all()[1].category
        context['category1'] = category_1
        context['category2'] = category_2
        context['special_category_1'] = Product.objects.filter(category=category_1)
        context['special_category_2'] = Product.objects.filter(category=category_2)
        return context

