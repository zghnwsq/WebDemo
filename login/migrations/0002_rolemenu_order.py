# Generated by Django 2.1.5 on 2019-02-26 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolemenu',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
