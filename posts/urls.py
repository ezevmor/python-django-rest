from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from posts.api import PostViewSet
from posts.views import HomeView, PostView, CreatePostView


router = DefaultRouter()
router.register('api/1.0/post', PostViewSet, base_name='api_post')


urlpatterns = [

    # WEB URLS
    url(r'^$', HomeView.as_view(), name='posts_home'),
    url(r'^blogs/(?P<pk>[0-9]+)/(?P<id>[0-9]+)$', PostView.as_view(), name='posts_post_detail'),
    url(r'^create_post$', CreatePostView.as_view(), name='posts_post_create'),

    # API URLS
    url(r'', include(router.urls))
]
