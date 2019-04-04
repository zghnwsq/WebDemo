from django.db import models
from django.contrib.auth.models import User
from projects.models import Projects
from testcase.models import TestCase
from datasource.models import Datasource

# Create your models here.

class TestPlan(models.Model):
    no = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Projects, on_delete=models.PROTECT)
    charge = models.ForeignKey(User('username'), on_delete=models.SET('Null'))
    case = models.ForeignKey(TestCase, on_delete=models.SET(''), null=True, blank=True)
    ds = models.ForeignKey(Datasource, on_delete=models.SET(''), null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    ds_range = models.CharField(max_length=72, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TP_Run_His(models.Model):
    testplan = models.ForeignKey(TestPlan, on_delete=models.PROTECT)
    case = models.ForeignKey(TestCase, on_delete=models.SET(''), null=True, blank=True)
    beg_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=20, null=True, blank=True)
    log_path = models.CharField(max_length=72, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)


class TP_Run_Detail(models.Model):
    his = models.ForeignKey(TP_Run_His, on_delete=models.CASCADE)
    ds_order = models.IntegerField()
    beg_time = models.CharField(max_length=20, null=True, blank=True)
    end_time = models.CharField(max_length=20, null=True, blank=True)
    result = models.CharField(max_length=20, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)





