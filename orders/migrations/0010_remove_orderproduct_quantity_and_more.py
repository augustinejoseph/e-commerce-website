# Generated by Django 4.1.6 on 2023-03-05 09:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0009_remove_orderproduct_productprice_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderproduct",
            name="quantity",
        ),
        migrations.RemoveField(
            model_name="orderproduct",
            name="variations",
        ),
    ]
