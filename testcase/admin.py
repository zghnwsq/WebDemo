from django.contrib import admin
from testcase.models import TestCase

# Register your models here.

class TestcaseAdmin(admin.ModelAdmin):
    list_display = ('case', 'project', 'charge', 'ds')

admin.site.register(TestCase, TestcaseAdmin)
