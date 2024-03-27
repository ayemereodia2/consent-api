# Generated by Django 5.0.3 on 2024-03-27 02:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quickstart", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="caregiver",
            name="consent",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="caregivers",
                to="quickstart.consent",
            ),
        ),
        migrations.AlterField(
            model_name="caregivertype",
            name="consent",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="caregiver_types",
                to="quickstart.consent",
            ),
        ),
    ]
