from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Profile


class InlineUser(admin.StackedInline):
    model = Profile


class NewUserAdmin(admin.ModelAdmin):
    inlines = (InlineUser,)
    list_display = ('username', 'id', 'email', 'is_active', 'is_superuser',)
    fieldsets = (
        ("Descripcion", {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'is_active')
        }),
    )


admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)

