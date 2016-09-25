from django.conf.urls import url, include
from django.contrib import admin

from posts import urls as posts_urls
from users import urls as users_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(posts_urls)),
    url(r'', include(users_urls))
]
