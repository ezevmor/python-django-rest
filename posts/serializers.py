from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post


class PostListSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        fields = ('title', 'url', 'description', 'created_at')
