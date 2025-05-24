# apps/posts/admin.py
from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'post_type', 'eco_points_earned', 'created_at']
    list_filter = ['post_type', 'created_at', 'group']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']