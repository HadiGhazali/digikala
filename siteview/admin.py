from django.contrib import admin

# Register your models here.
from siteview.models import SlideShow, BrandIntroduction, Special, SpecialCategory

admin.site.register(SlideShow)
admin.site.register(BrandIntroduction)
admin.site.register(Special)
admin.site.register(SpecialCategory)
