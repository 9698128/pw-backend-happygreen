# apps/posts/models.py
from django.db import models
from django.contrib.auth import get_user_model
from apps.groups.models import EcoGroup

User = get_user_model()


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('scan', 'Object Scan'),
        ('challenge', 'Challenge Completion'),
        ('tip', 'Eco Tip'),
        ('achievement', 'Achievement'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(EcoGroup, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    content = models.TextField()
    image_url = models.CharField(max_length=500, blank=True, null=True, help_text="URL dell'immagine")
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    eco_points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post_type}"

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

    class Meta:
        unique_together = ('post', 'user')  # Un utente può mettere like solo una volta per post
        ordering = ['-created_at']