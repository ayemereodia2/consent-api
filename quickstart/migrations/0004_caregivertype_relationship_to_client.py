# Generated by Django 5.0.3 on 2024-03-29 01:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quickstart", "0003_consentpackage_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="caregivertype",
            name="relationship_to_client",
            field=models.CharField(default="name of relationship", max_length=155),
            preserve_default=False,
        ),
    ]
