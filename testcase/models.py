from django.db import models
from django.contrib.auth.models import User
from projects.models import Projects
from datasource.models import Datasource

# Create your models here.


class TestCase(models.Model):
    no = models.CharField(max_length=20)
    case = models.CharField(max_length=50)
    project = models.ForeignKey(Projects, on_delete=models.PROTECT)
    charge = models.ForeignKey(User('username'), on_delete=models.SET('Null'))
    path = models.CharField(max_length=72, null=True, blank=True)
    sheet = models.CharField(max_length=32, null=True, blank=True)
    ds = models.ForeignKey(Datasource, on_delete=models.SET('Null'), null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.case


