from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Wishlist
from django.views.generic.list import ListView
from products.models import Product
from django.contrib import messages
from products.models import Variations
from cart.models import CartItem, Cart
from cart.views import _cartId



class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'wishlist.html'
    context_object_name = 'wishlist'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    


def addWishlist(request, productId): # changed function name to snake_case and variable name to snake_case
    product = Product.objects.get(id=productId) # changed variable name to snake_case
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            try:
                wishlist = Wishlist.objects.get(user=user)
            except Wishlist.DoesNotExist: # specified the exception to handle
                wishlist = Wishlist.objects.create(user=user, wished_item=product)
            wishlist.wished_item = product # fixed variable name
            wishlist.save() # added save method
        else:
            return redirect('login')
    return redirect( 'wishlist')

def removeWishlist(request, productId):
    product = Product.objects.get(id = productId)
    user = request.user
    if request.method =='POST':
        if user.is_authenticated:
            try:
                wishlist = Wishlist.objects.get(user = user , wished_item = product)
                wishlist.delete()
            except:
                pass
        else:
            return redirect('login')
    return redirect('wishlist')
            

def addCart(request, productId):
    current_user = request.user
    product = Product.objects.get(id=productId) #get the product

    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                print(value)
                try:
                    variation = Variations.objects.get(product=product, variationValue__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        is_cartItem_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        print('inside cart item exists', is_cartItem_exists)
        if is_cartItem_exists:
            cartItems = CartItem.objects.filter(product=product, user=current_user)  # get all cart items with the same product
            ex_var_list = []
            id = []
            for item in cartItems:
                existing_variation = item.variations.all()
                print('existing variation', existing_variation)
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity of the first item with the same variation
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                print('insde cart item exists else block')
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cartItem = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cartItem.variations.clear()
                cartItem.variations.add(*product_variation)
            cartItem.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variations.objects.get(product=product, variationCategory__iexact=key, variationValue__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cartId=_cartId(request)) # get the cart using the cartId present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cartId = _cartId(request)
            )
        cart.save()

        is_cartItem_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        
        if is_cartItem_exists:
            cartItems = CartItem.objects.filter(product=product, cart=cart)  # get all cart items with the same product
            ex_var_list = []
            id = []
            for item in cartItems:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity of the first item with the same variation
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                cartItem = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
                if len(product_variation) > 0:
                    cartItem.variations.clear()
                    cartItem.variations.add(*product_variation)
                cartItem.save()
            return redirect('cart')


