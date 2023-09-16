from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthorOrReadOnly
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Comment, Group, Post


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    Получаем список всех постов или создаем новый пост.
    Получаем, редактируем или удаляем пост по id.
    """

    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadOnly,
    ]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получаем список всех групп или создаем новую группу.
    Получаем, редактируем или удаляем группу по id.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получаем список всех всех комментариев поста с id=post_id или
    создаём новый, указав id поста, который хотим прокомментировать.
    Получаем, редактируем или удаляем комментарий по id у поста с id=post_id.
    """

    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadOnly,
    ]

    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        post = self.get_post()
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=self.get_post())
