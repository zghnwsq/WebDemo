# Generated by Django 2.1.7 on 2019-03-28 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testcase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='no',
            field=models.CharField(max_length=20),
        ),
    ]