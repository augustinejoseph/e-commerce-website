# Generated by Django 4.1.6 on 2023-03-05 13:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0012_remove_order_paymentmethod_orderproduct_payment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="paymentMethod",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
