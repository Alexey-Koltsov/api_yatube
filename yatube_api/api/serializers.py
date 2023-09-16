from rest_framework import serializers

from posts.models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью POST."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Group."""

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)
