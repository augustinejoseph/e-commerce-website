# Generated by Django 4.1.6 on 2023-02-23 13:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0005_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="expiry",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
