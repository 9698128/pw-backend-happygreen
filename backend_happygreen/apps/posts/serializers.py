# apps/posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model
from apps.groups.serializers import EcoGroupSerializer  # ← AGGIORNATO: EcoGroupSerializer

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_username', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'user_username', 'created_at']
        read_only_fields = ['user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    group_details = EcoGroupSerializer(source='group', read_only=True)  # ← AGGIORNATO
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'user_username', 'group', 'group_details',
            'content', 'image_url', 'post_type', 'eco_points_earned',
            'created_at', 'comments', 'likes', 'likes_count', 'comments_count'
        ]
        read_only_fields = ['user', 'created_at', 'eco_points_earned']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['group', 'content', 'image_url', 'post_type']

    def create(self, validated_data):
        # Calcola punti eco in base al tipo di post
        eco_points_map = {
            'scan': 10,
            'challenge': 25,
            'tip': 5,
            'achievement': 50
        }

        validated_data['eco_points_earned'] = eco_points_map.get(
            validated_data.get('post_type'), 0
        )

        return super().create(validated_data)