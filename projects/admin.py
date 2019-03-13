from django.contrib import admin
from .models import Projects, ProjectsUser

# Register your models here.

class ProjectsUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')

admin.site.register(Projects)
admin.site.register(ProjectsUser, ProjectsUserAdmin)
