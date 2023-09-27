# Generated by Django 4.1.6 on 2023-02-14 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Products",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("productName", models.CharField(max_length=200, unique=True)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("productDescription", models.TextField(max_length=1000)),
                ("price", models.IntegerField()),
                ("images", models.ImageField(upload_to="photos/products")),
                ("isAvailable", models.BooleanField(default=True)),
                ("stock", models.IntegerField()),
                ("createdDate", models.DateTimeField(auto_now_add=True)),
                ("modifiedDate", models.DateTimeField()),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="category.category",
                    ),
                ),
            ],
        ),
    ]
