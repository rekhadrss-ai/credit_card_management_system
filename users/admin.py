from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AdminLog


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (('Extra', {'fields': ('phone',)}),)


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'action', 'created_at')