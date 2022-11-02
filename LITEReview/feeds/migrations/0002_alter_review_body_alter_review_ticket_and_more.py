# Generated by Django 4.1.2 on 2022-11-02 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("feeds", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="body",
            field=models.TextField(blank=True, max_length=8192),
        ),
        migrations.AlterField(
            model_name="review",
            name="ticket",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="feeds.ticket"
            ),
        ),
        migrations.AlterField(
            model_name="ticket", name="title", field=models.CharField(max_length=128),
        ),
    ]
