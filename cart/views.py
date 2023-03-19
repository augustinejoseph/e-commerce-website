from decimal import Decimal
from time import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from accounts.models import Address
from products.models import Product, Variations
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from products.models import Variations
from django.http import JsonResponse
from .models import Coupon
from .forms import CouponApplyForm
from datetime import datetime
from pytz import timezone 
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
import razorpay
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from cart import utils
from django.http import JsonResponse
from accounts.models import Address
now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())

def get_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id, account=request.user)
        return JsonResponse({
            "firstName": address.firstName,
            "lastName": address.lastName,
            "email": address.email,
            "phone": address.phone,
            "addressLineOne": address.addressLineOne,
            "addressLineTwo": address.addressLineTwo,
            "city": address.city,
            "state": address.state,
            "country": address.country,
        })
    except Address.DoesNotExist:
        return JsonResponse({"error": "Address not found"})

def _cartId(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

class CartView(TemplateView):
    
    template_name = 'cart.html'
    def get(self, request):
        try:
            total=0
            quantity=0
            cartItems=None
            tax=0
            cartItems=0
            grandTotal=0
            if request.user.is_authenticated:
                cartItems = CartItem.objects.filter(user=request.user, isActive=True)
            else:
                cart = Cart.objects.get(cartId=_cartId(request))
                cartItems = CartItem.objects.filter(cart=cart, isActive=True)
            total = utils.total(cartItems) or 0 
            quantity = utils.quantity(cartItems) or 0
            tax = utils.tax(total)
            grandTotal = utils.grandTotal(total,tax)
        except ObjectDoesNotExist:
             pass

        context = {
            'total': total,
            'quantity': quantity,
            'cartItems': cartItems,
            'tax': tax,
            'grandTotal': grandTotal,
            
        }
        return render(request, 'cart.html', context)

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

def removeCartItem(request, productId , cartItemId):
    product = get_object_or_404(Product, id=productId)
    if request.user.is_authenticated:
        cartItem = CartItem.objects.get(product=product, user=request.user, id=cartItemId)
    else:
        cart        = Cart.objects.get(cartId = _cartId(request))
        cartItem    = CartItem.objects.get(product=product, cart=cart)
    cartItem.delete()
    return redirect('cart')

def removeCart(request, productId, cartItemId):

    product = get_object_or_404(Product, id=productId)
    try:
        if request.user.is_authenticated:
            cartItem = CartItem.objects.get(product=product, user=request.user, id=cartItemId)
            if cartItem.quantity > 1:
                cartItem.quantity -= 1
                cartItem.save()
            else:
                cartItem.delete()
        else:
        
            cart = Cart.objects.get(cartId=_cartId(request))
            cartItem = CartItem.objects.get(product=product, cart=cart, id=cartItemId)
            print(cartItem)
            if cartItem.quantity > 1:
                cartItem.quantity -= 1
                cartItem.save()
            else:
                cartItem.delete()
    except:
        pass
        print('except')
    return redirect('cart')

class CheckoutView(LoginRequiredMixin, View):
    success_url = reverse_lazy('checkout')

    def get(self, request):
        
        try:
            tax = 0
            grand_total = 0
            total = 0
            quantity = 0
            cartItems = None
            discount_amount = 0
            discount_percentage = 0
            coupon_id = request.session.get('coupon_id')

            if self.request.user.is_authenticated:
                cartItems = CartItem.objects.filter(user=self.request.user, isActive=True)
            else:
                cart = Cart.objects.get(cartId=_cartId(self.request))
                cartItems = CartItem.objects.filter(cart=cart, isActive=True)
            
            total =  utils.total(cartItems)
            quantity = utils.quantity(cartItems)
            tax = utils.tax(total)
            total_with_tax = int(total + tax)
            if coupon_id:
                coupon = Coupon.objects.get(id=coupon_id)
                discount_percentage = coupon.discount
                discount_amount = utils.discount_amount(total_with_tax, discount_percentage)
                grand_total = int(total_with_tax - discount_amount)
                order_amount = int(grand_total*100)
                order_currency = 'INR'
                order_receipt = 'order_receipt'
                request.session.update({
                    'grand_total': grand_total,
                    'discount_amount': discount_amount,
                    'total_with_tax': total_with_tax,
                })
            else:
                grand_total = int(total_with_tax)
                order_amount = int(grand_total*100)
                order_currency = 'INR'
                order_receipt = 'order_receipt'
                request.session['grand_total'] = grand_total
                request.session['discount_amount'] = discount_amount
                request.session['total_with_tax'] = total_with_tax

                
            
        except ObjectDoesNotExist:
            pass 

        addresses =Address.objects.filter(account = request.user)
        print(addresses)

        context = {
            'total': total,
            'quantity': quantity,
            'cartItems': cartItems,
            'tax': tax,
            'grandTotal': grand_total,
            'couponForm': CouponApplyForm(),
            'discount_amount' : discount_amount,
            'total_with_tax' : total_with_tax,
            'discount_percentage': discount_percentage,
            'addresses' : addresses,

            # Razorpay
            
            'order_amount': order_amount,
            'order_currency': order_currency,
            'order_receipt': order_receipt,

        }
        return render(request, 'checkout.html', context)

    def post(self, request):
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code, expiry__gt=now)
                request.session['coupon_id'] = coupon.id
                messages.success(request, 'Coupon Applied Successfully')
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
                messages.error(request, 'Invalid Coupon. Try agian with another code')
        return redirect('checkout')



