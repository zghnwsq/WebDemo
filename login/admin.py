from django.contrib import admin
from .models import Menu, RoleMenu

# Register your models here.


class MenuAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_text', 'url')


class RoleMenuAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'menu')


admin.site.register(Menu, MenuAdmin)
admin.site.register(RoleMenu, RoleMenuAdmin)
