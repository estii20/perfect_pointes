from django.contrib import admin
from .models import Category, PointeShoeBrand, PointeShoe, PointeShoeProduct

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

@admin.register(PointeShoe)
class PointeShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 
                    'sku', 
                    'size', 
                    'brand', 
                    'width', 
                    'shank', 
                    'color', 
                    'price', 
                    'status', 
                    'arch', 
                    'link', 
                    'ribbon', 
                    'image', 
                    'image_url')

@admin.register(PointeShoeProduct)
class PointeShoeProductAdmin(admin.ModelAdmin):
    list_display = ('title', 
                    'pointe_shoe', 
                    'brand', 
                    'availability', 
                    'sku')
    
    ordering = ('sku',)

