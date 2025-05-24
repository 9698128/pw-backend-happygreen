from django.db import models
from apps.authentication.models import CustomUser

class ObjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    recycling_info = models.TextField()
    environmental_impact = models.TextField()
    sustainability_tips = models.TextField()
    decomposition_time = models.CharField(max_length=100, blank=True)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Object Categories"

    def __str__(self):
        return self.name

class ScannedObject(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scanned_objects')
    image = models.ImageField(upload_to='scanned_objects/')
    detected_object = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    eco_points_earned = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.detected_object} scanned by {self.user.username}"

class ProductBarcode(models.Model):
    barcode = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(ObjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_eco_friendly = models.BooleanField(default=False)
    sustainability_score = models.IntegerField(default=0, help_text="Score from 0-100")
    recycling_instructions = models.TextField(blank=True)
    eco_alternatives = models.TextField(blank=True)
    environmental_impact = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} - {self.barcode}"

class BarcodeSearch(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='barcode_searches')
    barcode = models.ForeignKey(ProductBarcode, on_delete=models.CASCADE)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched {self.barcode.product_name}"