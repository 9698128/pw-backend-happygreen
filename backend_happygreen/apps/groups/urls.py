# apps/groups/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.EcoGroupListCreateView.as_view(), name='group-list-create'),
    path('<int:pk>/', views.EcoGroupDetailView.as_view(), name='group-detail'),
    path('join/<str:invite_code>/', views.join_group, name='join-group'),
    path('<int:group_id>/leave/', views.leave_group, name='leave-group'),
]