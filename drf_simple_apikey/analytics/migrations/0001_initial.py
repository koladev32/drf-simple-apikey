# Generated by Django 5.0.6 on 2024-05-22 22:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("drf_simple_apikey", "0002_alter_apikey_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApiKeyAnalytics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("request_number", models.IntegerField(default=0)),
                ("accessed_endpoints", models.JSONField(default=dict)),
                (
                    "api_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analytics",
                        to="drf_simple_apikey.apikey",
                    ),
                ),
            ],
        ),
    ]
