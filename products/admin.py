from django.contrib import admin
from .models import Product, Category, Product_Family


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'active',
        'SKU',
        'name',
        'product_family',
        'category',
        'image',
        'size',
        'pack',
        'price',
        'description',
        'created',
        'modified',
    )

    ordering = ('product_family',)
    search_fields = ['product_family', 'name', 'description']
    list_filter = ('active', 'category', 'category__division')


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
