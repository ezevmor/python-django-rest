from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from users.api import UserViewSet, BlogViewSet
from users.views import BlogsListView, BlogDetailView, LoginView, LogoutView, SignupView


router = DefaultRouter()
router.register('api/1.0/users', UserViewSet, base_name='api_users_')
router.register('api/1.0/blogs', BlogViewSet, base_name='api_blogs_')


urlpatterns = [

    #WEB URLS
    url(r'^blogs/$', BlogsListView.as_view(), name='users_blog_list'),
    url(r'^blogs/(?P<pk>[0-9]+)$', BlogDetailView.as_view(), name="users_blog_detail"),
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),
    url(r'^signup$', SignupView.as_view(), name='users_signup'),

    #API URLS
    url(r'', include(router.urls))
]
