from datetime import timezone
import datetime
from django.utils.timezone import now
from django.db import models
from products.models import Product, Variations
from accounts.models import Account


class Cart(models.Model):
    cartId = models.CharField(max_length=100, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.cartId


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cartItem"
    )
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    isActive = models.BooleanField(default=True)
    variations = models.ManyToManyField(Variations, blank=True)

    def __unicode__(self):
        return self.product

    def subTotal(self):
        return self.product.price * self.quantity


now = datetime.datetime.now()


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=2, decimal_places=0)
    expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.code


class UserCoupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user
