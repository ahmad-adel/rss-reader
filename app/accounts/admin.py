from django.contrib import admin
from .models import Token, User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ['pk', 'email',]
    fields = ('email', 'password')
    fieldsets = ()
    search_fields = ['email']


admin.site.register(Token)
admin.site.register(User, CustomUserAdmin)
