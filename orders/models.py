from django.db import models
from accounts.models import Account
from products.models import Product, Variations

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    paymentId = models.CharField(max_length=100)
    amountPaid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    paymentMethod = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.paymentId


status = (
    ("New", "New"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
    ("Refunded", "Refunded"),
)


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    orderNumber = models.CharField(max_length=30)
    dateCreated = models.DateTimeField(auto_now_add=True)
    orderTotal = models.FloatField()
    tax = models.FloatField(default="18")
    status = models.CharField(choices=status, default="New", max_length=50)
    isOrdered = models.BooleanField(default=False)
    refund = models.CharField(max_length=100, blank=True, null=True, default=None)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default="email")
    phone = models.CharField(max_length=100, default="phone")
    addressLineOne = models.CharField(
        max_length=100, blank=True, null=True, default=None
    )
    addressLineTwo = models.CharField(
        max_length=100, blank=True, null=True, default=None
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True, default=None)
    orderNote = models.TextField(max_length=1000, blank=True, null=True, default=None)

    createdAt = models.DateTimeField(auto_now=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def fullName(self):
        return f"{self.firstName} {self.lastName}"

    def fullAddress(self):
        return f"{self.addressLineOne} {self.addressLineTwo} {self.city} {self.state} {self.country}"

    def __str__(self):
        return f"Order {self.id}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    Payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    variations = models.ManyToManyField(Variations, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    productPrice = models.FloatField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.productName
