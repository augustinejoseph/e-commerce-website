# Generated by Django 4.1.6 on 2023-03-11 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]