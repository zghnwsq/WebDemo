from django.db import models
from django.contrib.auth.models import User
from projects.models import Projects

# Create your models here.


class Datasource(models.Model):
    no = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Projects, on_delete=models.PROTECT)
    charge = models.ForeignKey(User('username'), on_delete=models.SET('Null'))
    path = models.CharField(max_length=72)
    sheet = models.CharField(max_length=32)
    length = models.IntegerField()
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
