# Generated by Django 4.1.2 on 2022-10-23 20:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="UserProfile", new_name="Profile",),
    ]