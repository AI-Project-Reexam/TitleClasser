# Generated by Django 4.2.11 on 2024-03-22 13:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_panel", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelInfo",
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
                ("conf_matrix", models.CharField(max_length=255)),
                ("training_time", models.CharField(max_length=255)),
                ("old_acc", models.FloatField(null=True)),
                ("accuracy", models.FloatField()),
                ("precision", models.FloatField()),
                ("recall", models.FloatField()),
                ("f_one", models.FloatField()),
            ],
        ),
    ]
