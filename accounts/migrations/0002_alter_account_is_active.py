# Generated by Django 4.1.6 on 2023-02-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
