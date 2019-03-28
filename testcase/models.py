from django.db import models
from django.contrib.auth.models import User
from projects.models import Projects
from datasource.models import Datasource

# Create your models here.

class TestCase(models.Model):
    no = models.CharField(max_length=32)
    case = models.CharField(max_length=50)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    charge = models.ForeignKey(User('username'), on_delete=models.CASCADE)
    path = models.CharField(max_length=72)
    sheet = models.CharField(max_length=32)
    ds = models.ForeignKey(Datasource, on_delete=models.CASCADE)

    def __str__(self):
        return self.case


