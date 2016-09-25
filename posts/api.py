from django.db.models import Q
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, VISIBILITY_PUBLIC
from posts.serializers import PostSerializer, PostListSerializer


class PostQueryset(object):
    @staticmethod
    def get_posts_by_user(user):
        possible_posts = Post.objects.all().select_related("owner")
        if not user.is_authenticated():
            possible_posts = possible_posts.filter(visibility=VISIBILITY_PUBLIC)
        elif not user.is_superuser:
            possible_posts = possible_posts.filter(Q(visibility=VISIBILITY_PUBLIC) | Q(owner=user))
        return possible_posts.order_by('-created_at')


class PostViewSet(ModelViewSet):
    """
    Endpoint de gestion de posts
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    search_fields = ('title', 'content',)
    order_fields = ('title', 'created_at')
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)

    def get_queryset(self):
        return PostQueryset.get_posts_by_user(self.request.user)

    def get_serializer_class(self):
        return PostSerializer if self.action != 'list' else PostListSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(owner=self.request.user)
