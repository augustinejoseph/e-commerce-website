# Generated by Django 4.1.6 on 2023-03-12 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_address_account_address_addresslineone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='wallet',
            field=models.IntegerField(default=0),
        ),
    ]