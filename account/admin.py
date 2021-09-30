from django.contrib import admin
from django.contrib.auth.models import Group as AuthGroup

# Register your models here.
from account.models import User, Role

admin.site.unregister(AuthGroup)

admin.site.site_header = "Tech3 Admin"
admin.site.site_title = "Tech3 Admin Portal"
admin.site.index_title = "Welcome to Tech3 Researcher Portal"


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'phone', 'first_name', 'last_name', 'is_active', 'mode', 'role', 'is_superuser', 'modified_by')
    search_fields = ('first_name',)
