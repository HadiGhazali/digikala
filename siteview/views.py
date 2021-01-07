from django.shortcuts import render
from django.views.generic import TemplateView

from .models import SlideShow


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        context['slide_list'] = SlideShow.objects.all()
        return context

