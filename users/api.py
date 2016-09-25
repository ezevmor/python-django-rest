from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet, ModelViewSet
from users.models import Profile
from users.permissions import UserPermission
from users.serializers import UserSerializer, UserListSerializer, BlogSerializer


class UserViewSet(ViewSet):
    """
    Endpoint de gestion de usuarios
    """
    permission_classes = (UserPermission,)

    def list(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def retreave(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class BlogViewSet(ModelViewSet):
    """
    Endpoint de listado de blogs
    """
    search_fields = ('blog_name',)
    order_fields = ('blog_name',)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)

    def get_queryset(self):
        blogs = Profile.objects.filter(visible_blog=True)
        return blogs

    def get_serializer_class(self):
        return BlogSerializer
