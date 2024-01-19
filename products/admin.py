from django.contrib import admin
from .models import Category, PointeShoeBrand, PointeShoe, Size, Width, PointeShoeProduct, Color


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 
                    'description', 
                    'friendly_name')


@admin.register(PointeShoeBrand)
class PointeShoeBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 
                    'description', 
                    'logo', 
                    'category', 
                    'friendly_name', 
                    'sku')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size',)


@admin.register(Width)
class WidthAdmin(admin.ModelAdmin):
    list_display = ('width',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')


@admin.register(PointeShoe)
class PointeShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 
                    'sku', 
                    'brand', 
                    'width', 
                    'shank', 
                    'color', 
                    'price', 
                    'status', 
                    'arch', 
                    'link', 
                    'ribbon', 
                    'feature', 
                    'category')
    filter_horizontal = ('available_sizes', 'available_widths')


@admin.register(PointeShoeProduct)
class PointeShoeProductAdmin(admin.ModelAdmin):
    list_display = ('title', 
                    'pointe_shoe', 
                    'brand', 
                    'availability', 
                    'sku', 
                    'image_url')
    search_fields = ('title', 'pointe_shoe__name', 'brand__name')
