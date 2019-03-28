from django.db import models
from django.contrib.auth.models import Group
# Create your models here.


class Menu(models.Model):
    order = models.IntegerField(unique=True)
    menu_text = models.CharField(max_length=20, unique=True)
    url = models.CharField(max_length=32)

    def __str__(self):
        return self.menu_text


class RoleMenu(models.Model):
    role_name = models.ForeignKey(Group, to_field='name', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, to_field='menu_text', on_delete=models.CASCADE)
