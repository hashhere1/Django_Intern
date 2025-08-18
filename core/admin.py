from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.models import Product
from store.admin import ProductAdmin
from tags.models import TaggedItem
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # REQUIRED FOR ADD USER PAGE (your existing code)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

class TagInLine(GenericTabularInline):
    autocomplete_fields = ["tag"]
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
