# Generated by Django 4.1.6 on 2023-02-25 09:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0004_order_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="createdAt",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="order",
            name="modifiedAt",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
