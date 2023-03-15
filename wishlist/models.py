from django.db import models
from accounts.models import Account
from products.models import Product

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    wished_item = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True) # changed field name to snake_case
    created_at =  models.DateTimeField(auto_now_add=True)

    def __srt__(self):
        return self.user
    

