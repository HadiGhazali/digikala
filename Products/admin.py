from django.contrib import admin

# Register your models here.
from Products.models import Category, Comment, Brand, Product, ProductImage, ProductMeta, ShopProduct, Like, HitCount, \
    UrlHit


class ChildrenItemInline(admin.TabularInline):
    model = Category
    fields = (
        'title', 'slug'
    )
    extra = 1
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'parent')
    search_fields = ('slug', 'title')
    list_filter = ('parent',)
    inlines = [
        ChildrenItemInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('product',)
    date_hierarchy = 'create_at'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    show_change_link = True


class ProductMetaInline(admin.TabularInline):
    model = ProductMeta
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'brand')
    search_fields = ('name',)
    date_hierarchy = 'create_at'
    inlines = (ProductImageInline, ProductMetaInline)


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'check_status')
    search_fields = ('shop', 'product')


admin.site.register(Like)
admin.site.register(HitCount)
admin.site.register(UrlHit)
