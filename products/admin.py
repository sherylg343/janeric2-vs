from django.contrib import admin
from .models import Product, Category, Product_Family, ProductSize


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'active',
        'SKU',
        'name',
        'product_family',
        'category',
        'image',
        'product_size',
        'pack',
        'price',
        'description',
        'created',
        'modified',
    )

    ordering = ('product_family',)
    list_filter = ('active', 'category', 'category__division')


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name'
    )

    ordering = ('name',)


class Product_FamilyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand_name'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'division'
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product_Family, Product_FamilyAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
