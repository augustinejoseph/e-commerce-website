# Generated by Django 4.1.6 on 2023-02-25 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_address_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='name',
            new_name='account',
        ),
    ]
