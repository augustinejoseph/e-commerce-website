# Generated by Django 4.1.6 on 2023-03-05 17:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0009_rename_name_address_account"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="address",
            name="city",
        ),
        migrations.RemoveField(
            model_name="address",
            name="country",
        ),
        migrations.RemoveField(
            model_name="address",
            name="pincode",
        ),
        migrations.RemoveField(
            model_name="address",
            name="state",
        ),
        migrations.RemoveField(
            model_name="address",
            name="streetAddress",
        ),
    ]
