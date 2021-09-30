from django.contrib import admin

# Register your models here.
from account.models import User, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'phone', 'first_name', 'last_name', 'is_active', 'mode', 'role', 'is_superuser', 'modified_by')
    search_fields = ('first_name',)
