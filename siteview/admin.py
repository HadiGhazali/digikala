from django.contrib import admin

# Register your models here.
from siteview.models import SlideShow, BrandIntroduction

admin.site.register(SlideShow)
admin.site.register(BrandIntroduction)
