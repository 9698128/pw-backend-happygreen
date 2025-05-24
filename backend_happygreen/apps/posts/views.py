# apps/posts/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from .serializers import PostSerializer, CreatePostSerializer, CommentSerializer
from apps.groups.models import EcoGroup

User = get_user_model()


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePostSerializer
        return PostSerializer

    def get_queryset(self):
        # Mostra post dai gruppi di cui l'utente fa parte
        user_groups = EcoGroup.objects.filter(members=self.request.user)
        return Post.objects.filter(group__in=user_groups).distinct()

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)

        # Aggiungi punti eco all'utente
        self.request.user.eco_points += post.eco_points_earned
        self.request.user.save()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)

    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request, user_id=None):
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            posts = Post.objects.filter(user=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        posts = Post.objects.filter(user=request.user)

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)