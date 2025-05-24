from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('badges/', views.user_badges, name='user_badges'),
    path('badges/available/', views.available_badges, name='available_badges'),
    path('award-points/', views.award_points, name='award_points'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]