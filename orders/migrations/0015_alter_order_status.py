# Generated by Django 4.1.6 on 2023-03-06 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0014_alter_orderproduct_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("New", "New"),
                    ("Completed", "Completed"),
                    ("Cancelled", "Cancelled"),
                    ("Pending", "Pending"),
                    ("Processing", "Processing"),
                    ("Refunded", "Refunded"),
                    ("Failed", "Failed"),
                ],
                default="New",
                max_length=50,
            ),
        ),
    ]
