from django.db import models
from django.urls import reverse
from accounts.models import Account


brand = (
    ("adidas", "Adidas"),
    ("nike", "Nike"),
    ("reebok", "Reebok"),
    ("redchief", "Redchief"),
    ("seeandwear", "See and wear"),
    ("uspolo", "US Polo"),
    ("leecooper", "Lee Cooper"),
    ("campus", "Campus"),
    ("bata", "Bata"),
    ("crocs", "Crocs"),
    ("mactree", "Mactree"),
)


class Product(models.Model):
    productName = models.CharField(max_length=200, unique=True)
    brand = models.CharField(max_length=100, null=True, choices=brand)
    slug = models.SlugField(max_length=200, unique=True)
    productDescription = models.TextField(max_length=1000)
    price = models.IntegerField()
    images = models.ImageField(upload_to="photos/products")
    isAvailable = models.BooleanField(default=True)
    stock = models.IntegerField()
    category = models.ForeignKey(
        "category.Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.productName

    def productUrl(self):
        return reverse("ProductDetails", args=[self.category.slug, self.slug])


class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(
            variationCategory="size", isAvailable=True
        )


variationChoices = (("size", "size"),)


class Variations(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variations"
    )
    variationCategory = models.CharField(max_length=100, choices=variationChoices)
    variationValue = models.CharField(max_length=50)
    isAvailable = models.BooleanField(default=True)
    createdAt = models.DateField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variationValue


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="store/products", max_length=255)

    def __str__(self):
        return self.product.productName

    class Meta:
        verbose_name = "productgallery"
        verbose_name_plural = "prodcut gallery"


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
