from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.ObjectCategoryListView.as_view(), name='object_categories'),
    path('scanned/', views.ScannedObjectListCreateView.as_view(), name='scanned_objects'),
    path('scanned/user/', views.UserScannedObjectsView.as_view(), name='user_scanned_objects'),
    path('barcode/search/', views.search_barcode, name='search_barcode'),
    path('barcode/history/', views.user_barcode_searches, name='barcode_history'),
    path('classify-waste/', views.classify_waste, name='classify_waste'),
]