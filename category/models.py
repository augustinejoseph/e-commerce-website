from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    categoryName = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "categories"

    def menuUrl(self):
        return reverse("productByCategory", args=[self.slug])

    def __str__(self):
        return self.categoryName
