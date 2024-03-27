# Generated by Django 5.0.3 on 2024-03-27 01:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Consent",
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
                ("consent_title", models.CharField(max_length=256)),
                ("client_name", models.CharField(max_length=256)),
                ("name_on_health_card", models.CharField(max_length=256)),
                ("health_card_number", models.CharField(max_length=155)),
                ("date_of_birth", models.DateTimeField(auto_now=True)),
                ("permission_to_communicate", models.BooleanField()),
                ("email_to_communicate_with", models.CharField(max_length=155)),
                ("contact_me", models.BooleanField()),
                ("date_of_signature", models.DateTimeField(auto_now=True)),
                ("pronouns", models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name="CareGiverType",
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
                ("institution_name", models.CharField(max_length=155)),
                ("relationship_to_client", models.CharField(max_length=155)),
                (
                    "consent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="quickstart.consent",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CareGiver",
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
                ("care_giver_name", models.CharField(max_length=155)),
                ("relationship_to_client", models.CharField(max_length=150)),
                (
                    "consent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="quickstart.consent",
                    ),
                ),
            ],
        ),
    ]