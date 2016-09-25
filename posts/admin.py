from django.contrib import admin
from posts.models import Post, Category


class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'visibility', 'owner_id')
    list_filter = ('visibility', 'owner_id')


admin.site.register(Post, PostsAdmin)
admin.site.register(Category)

