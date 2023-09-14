from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Comment, Group, Post


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    Получаем список всех постов или создаем новый пост.
    Получаем, редактируем или удаляем пост по id.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=HTTPStatus.NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    """
    Получаем список всех групп или создаем новую группу.
    Получаем, редактируем или удаляем группу по id.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=HTTPStatus.NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    """
    Получаем список всех всех комментариев поста с id=post_id или
    создаём новый, указав id поста, который хотим прокомментировать.
    Получаем, редактируем или удаляем комментарий по id у поста с id=post_id.
    """

    def get_queryset(self):
        post = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post=post)
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user,
                        post=get_object_or_404(Post, id=post_id))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTPStatus.CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=HTTPStatus.NO_CONTENT)
