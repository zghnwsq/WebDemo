from django.contrib import admin
from datasource.models import Datasource

# Register your models here.

class DatasourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'charge')

admin.site.register(Datasource, DatasourceAdmin)
