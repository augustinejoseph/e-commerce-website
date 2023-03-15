# Generated by Django 4.1.6 on 2023-03-01 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_email_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='addressLineTwo',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='orderNote',
            field=models.TextField(blank=True, default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.FloatField(default='18'),
        ),
        migrations.AlterField(
            model_name='order',
            name='addressLineOne',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
