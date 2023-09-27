from .models import Cart, CartItem
from .views import _cartId


def counter(request):
    cartCount = 0
    if "admin" in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cartId=_cartId(request))
            cartItems = CartItem.objects.all().filter()
            for cartItem in cartItems:
                cartCount += cartItem.quantity
        except Cart.DoesNotExist:
            cartCount = 0
    return dict(cartCount=cartCount)
