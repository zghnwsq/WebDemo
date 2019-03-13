from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Projects(models.Model):
    project = models.CharField(max_length=32)
    status = models.CharField(max_length=8)
    charge = models.ForeignKey(User('username'), on_delete=models.CASCADE)

    def __str__(self):
        return self.project


class ProjectsUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)

