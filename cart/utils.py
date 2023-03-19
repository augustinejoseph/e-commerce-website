from products.models import Product, Variations
from django.conf import settings
from cart.models import CartItem
from . import views


total=0
grandTotal = 0

def total(cartItems):
    total = 0
    quantity=0
    for item in cartItems:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
    return total

def quantity(cartItems):
    quantity=0
    total = 0
    for item in cartItems:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
        return quantity

def tax(total):
    return (.18*total)

def grandTotal(total, tax):
    return total+tax

def discount_amount(total_with_tax, discount_percentage):
    return int((total_with_tax*discount_percentage)/100)


