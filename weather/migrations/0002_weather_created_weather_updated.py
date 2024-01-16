# Generated by Django 5.0.1 on 2024-01-16 18:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="weather",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="weather",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
