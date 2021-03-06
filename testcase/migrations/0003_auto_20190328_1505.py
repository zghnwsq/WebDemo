# Generated by Django 2.1.7 on 2019-03-28 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testcase', '0002_auto_20190328_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='ds',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datasource.Datasource'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='path',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='sheet',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
