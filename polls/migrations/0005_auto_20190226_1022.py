# Generated by Django 2.1.5 on 2019-02-26 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_role_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='role',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
