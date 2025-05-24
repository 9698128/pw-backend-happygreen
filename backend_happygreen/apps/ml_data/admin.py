from django.contrib import admin
from .models import ObjectCategory, ScannedObject, ProductBarcode, BarcodeSearch

@admin.register(ObjectCategory)
class ObjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'decomposition_time']
    search_fields = ['name', 'description']

@admin.register(ScannedObject)
class ScannedObjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'detected_object', 'confidence_score', 'eco_points_earned', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['user__username', 'detected_object']

@admin.register(ProductBarcode)
class ProductBarcodeAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'brand', 'barcode', 'is_eco_friendly', 'sustainability_score']
    list_filter = ['is_eco_friendly', 'category', 'created_at']
    search_fields = ['product_name', 'brand', 'barcode']

@admin.register(BarcodeSearch)
class BarcodeSearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'barcode', 'searched_at']
    list_filter = ['searched_at']
    search_fields = ['user__username', 'barcode__product_name']