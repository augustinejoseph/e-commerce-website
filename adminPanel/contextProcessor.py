from accounts.models import Account
from products.models import Product
from category.models import Category
from orders.models import Order
from django.db.models import Sum


def countData(request):
    totalPrice = Order.objects.aggregate(Sum("orderTotal"))["orderTotal__sum"]
    print(totalPrice)
    return {
        "userCount": Account.objects.count(),
        "productCount": Product.objects.count(),
        "categoryCount": Category.objects.count(),
        "orderCount": Order.objects.count(),
        "totalPrice": totalPrice,
    }
