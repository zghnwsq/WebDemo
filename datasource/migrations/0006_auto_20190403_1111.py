# Generated by Django 2.1.5 on 2019-04-03 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasource', '0005_auto_20190402_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='path',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='sheet',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]