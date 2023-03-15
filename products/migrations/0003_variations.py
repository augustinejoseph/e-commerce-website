# Generated by Django 4.1.6 on 2023-02-18 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_products_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='variations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variationCategory', models.CharField(choices=[('size', 'size')], max_length=100)),
                ('variationName', models.CharField(max_length=50)),
                ('isAvailable', models.BooleanField(default=True)),
                ('createdAt', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
