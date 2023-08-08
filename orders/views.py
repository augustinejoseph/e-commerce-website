import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from cart.models import CartItem
import ecommerce.settings 
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from products.models import Product
import datetime, razorpay
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from cart import utils
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Payment Callback
@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        client = razorpay.Client(auth=(ecommerce.settings.RAZOR_KEY_ID, ecommerce.settings.RAZOR_KEY_SECRET))
        payment = client.payment.fetch(payment_id)
        amount = payment['amount']
        status = payment['status']

        print('-----------status-after-payment-redirect-to-callback',status)
        print('----------payment_id-form rzpay-server -redirect-to-callback', payment_id)
        print('-----------client-form rzpay-server after -redirect-to-callback',client)
        print('------------payment-form rzpay-server after -redirect-to-callback', payment)


        if status == 'captured':
            # Saving Payment
            payment = Payment(
            user = request.user,
            paymentMethod = 'Razorpay',
            paymentId = payment_id,
            amountPaid = amount,
            status =status,
            )
            payment.save()

            # Updating Order Table
            order_number = request.session.get('order_number', None)
            order = Order.objects.get(user=request.user, orderNumber = order_number)
            print('----------------------inside order in callback from rzpay', order)
            order.payment = payment
            print('----------------------inside payment in callback from rzpay', payment)
            order.isOrdered =True
            order.save()

        

            # Moving Cart items in Order Table
            cart_items = CartItem.objects.filter(user = request.user)
            for item in cart_items:
                orderProduct = OrderProduct()
                orderProduct.order_id = order.id
                orderProduct.Payment = payment
                orderProduct.user = request.user
                orderProduct.product_id = item.product_id
                orderProduct.quantity = item.quantity
                orderProduct.productPrice = item.product.price
                orderProduct.ordered = True
                orderProduct.save()

                cart_item = CartItem.objects.get(id = item.id)
                product_variation = cart_item.variations.all()
                orderProduct = OrderProduct.objects.get(id = orderProduct.id)
                orderProduct.variations.set(product_variation)
                orderProduct.save()

                # Reducing the quantity of items from Stock in warehouse
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            order = Order.objects.get(user=request.user, orderNumber = order_number)
            order.isOrdered = True
            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            total = utils.total(ordered_products)
            tax = utils.tax(total)
            grandTotal = total + tax

            context = {
                'order_number': order_number,
                'order': order,
                'ordered_products': ordered_products,
                'grandTotal' : grandTotal,
                'order' : order,
                }
            # Clearing the cart
            CartItem.objects.filter(user=request.user).delete()
        else:
            pass
        return render(request, 'paymentSuccess.html', context)
    else:
        # Return an HTTP response with a bad request status code
        return HttpResponse(status=400)

#sample comment
@login_required(login_url='login')
def payment(request):
    currentUser = request.user
    cartItems = CartItem.objects.filter(user = currentUser)
    cartCount = cartItems.count()
    if cartCount <=0:
        return redirect('home') 
    
 
    total = utils.total(cartItems)
    quantity = utils.quantity(cartItems)
    tax = utils.tax(total)
    grandTotal = request.session.get('grand_total', None)
    discount_amount = request.session.get('discount_amount', None)
    total_with_tax = request.session.get('total_with_tax', None)
    total_without_tax = total_with_tax-tax
    razorpayAmount = (grandTotal*100)
    RAZOR_KEY_ID = ecommerce.settings.RAZOR_KEY_ID
    print(RAZOR_KEY_ID, 'razorpay-key-id')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all related informations inside the table
            # data is a instance of the form
            data = Order() 
            data.user = currentUser
            data.firstName = form.cleaned_data['firstName']
            data.lastName = form.cleaned_data['lastName']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.addressLineOne = form.cleaned_data['addressLineOne']
            data.addressLineTwo = form.cleaned_data['addressLineOne']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.isOrdered = False
            data.orderTotal = grandTotal
            data.tax = tax
            data.save()
            # when the data is saved, it will create an foriegn key. 
            # Generating order number

            yr = int(datetime.date.today().strftime('%y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt, dt)
            currentDate = d.strftime("%y%m%d")

            # Concatinating current date and orderforms instance to get a unique order ID
            orderNumber = currentDate + str(data.id)
            data.orderNumber = orderNumber
            request.session['order_number'] = data.orderNumber
            data.save()

            order = Order.objects.get(user=request.user, orderNumber = orderNumber)
            client = razorpay.Client(auth=(ecommerce.settings.RAZOR_KEY_ID, ecommerce.settings.RAZOR_KEY_SECRET))
            payment = client.order.create({'amount':razorpayAmount , 'currency': 'INR', 'payment_capture': '1'})
            order_id = payment['id']
            
            context = {
                'cartItems' : cartItems,
                'order' : order,
                'total': total,
                'discount_amount': discount_amount,
                'grandTotal': grandTotal,
                'razorpayAmount' : razorpayAmount,
                'orderNumber' : orderNumber,
                'total_with_tax' : total_with_tax,
                'total_without_tax' : total_without_tax,
                'tax' : tax,
                'RAZOR_KEY_ID' : RAZOR_KEY_ID,
                'order_id' : order_id,
                }
            print(order, '-order-from-database')
            print(client, '-client-from-rzpy')
            print(payment,'-payment-from-rzpy')
            print(cartItems)
            print(RAZOR_KEY_ID, '-razoor-key-id')
            print(order_id, '-razoor-order_id-')
            print('------------------raz amound in paise', razorpayAmount)

            
            return render(request, 'payment.html', context)
    else:
        return redirect('checkout')            

def cod(request):
    cartItems = CartItem.objects.filter(user=request.user, isActive=True)
    total = utils.total(cartItems) or 0
    quantity = utils.quantity(cartItems) or 0
    tax = utils.tax(total) or 0
    grandTotal = total + tax
    # Saving Payment
    payment = Payment(
    user = request.user,
    paymentMethod = 'COD',
    amountPaid = grandTotal,
    status ='captured',
    )
    payment.save()

    # Updating Order Table
    order_number = request.session.get('order_number', None)
    order = Order.objects.get(user=request.user, orderNumber = order_number)
    print('----------------------inside order in callback from rzpay', order)
    order.payment = payment
    print('----------------------inside payment in callback from rzpay', payment)
    order.isOrdered =True
    order.save()



    # Moving Cart items in Order Table
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderProduct = OrderProduct()
        orderProduct.order_id = order.id
        orderProduct.Payment = payment
        orderProduct.user = request.user
        orderProduct.product_id = item.product_id
        orderProduct.quantity = item.quantity
        orderProduct.productPrice = item.product.price
        orderProduct.ordered = True
        orderProduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderProduct = OrderProduct.objects.get(id = orderProduct.id)
        orderProduct.variations.set(product_variation)
        orderProduct.save()

        # Reducing the quantity of items from Stock in warehouse
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    order = Order.objects.get(orderNumber=order_number)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    total = utils.total(ordered_products)
    print('-------------ordered products', ordered_products)
    # print('-----osrderd variation', ordered_products.variations)
    # for variation in ordered_products.variations.all():
    #     print('varistion===============================',variation)
    tax = utils.tax(total)
    grandTotal = total + tax

    context = {
        'order_number': order_number,
        'order': order,
        'ordered_products': ordered_products,
        'grandTotal' : grandTotal,
        'order' : order,
        }
    # Clearing the cart
    CartItem.objects.filter(user=request.user).delete()
    return render(request, 'paymentSuccess.html', context)

# Creating a Razorpay order from razorpay server
@csrf_exempt
def razorpay_payment(request):
    grandTotal = request.session.get('grand_total', None)
    if request.method == 'POST':
        amount = grandTotal*100
        print('-------------------------amound passed in order creation',amount)
        client = razorpay.Client(auth=(ecommerce.settings.RAZOR_KEY_ID, ecommerce.settings.RAZOR_KEY_SECRET))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, 'payment.html', {'payment': payment})
    return redirect('cart')
