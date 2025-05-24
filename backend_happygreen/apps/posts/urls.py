# apps/posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/like/', views.like_post, name='like-post'),
    path('<int:post_id>/comment/', views.add_comment, name='add-comment'),
    path('user/', views.user_posts, name='user-posts'),
    path('user/<int:user_id>/', views.user_posts, name='user-posts-by-id'),
]