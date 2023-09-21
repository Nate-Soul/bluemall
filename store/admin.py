from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.text import slugify

from .models import (Product,
                     Category,
                     ProductImage,
                     ProductSpecification,
                     ProductSpecificationValue,
                     ProductType
                     )



# Register your models here.
class CategoryAdmin(MPTTModelAdmin):
    list_display    = ['name', 'slug',]
    prepopulated_fields = {
        'slug': (slugify('name'),),
    }
    
admin.site.register(Category, CategoryAdmin)

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,        
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display    = ['title', 'price', 'discount_price', 'is_active', 'created', 'updated']
    list_filter     = ['is_active',]
    list_editable   = ['is_active', 'price', 'discount_price']
    prepopulated_fields = {
        'slug': (slugify('title'),),
    }
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
