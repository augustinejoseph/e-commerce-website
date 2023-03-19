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
            order.status = 'Completed'
            order.payment = payment

        

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
            # Clearing the cart
            CartItem.objects.filter(user=request.user).delete()
            cartItems = CartItem.objects.filter(user=request.user, isActive=True)
            total = utils.total(cart_items)
            tax = utils.tax(total)
            grandTotal = total + tax

            context = {
                'order_number': order_number,
                'order': order,
                'cartItems': cartItems,
                'grandTotal' : grandTotal,
                'order' : order,
                }
        else:
            pass
        return render(request, 'paymentSuccess.html', {'amount': amount, 'status': status})
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
    razorpayTotal = int(grandTotal*100)
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
            state = form.cleaned_data['state']
            print('-------------state',state)
            #rajyam = form.cleaned_data['rajyam']
            #print('-------------country',rajyam)
            data.isOrdered = True
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
            payment = client.order.create({'amount':grandTotal , 'currency': 'INR', 'payment_capture': '1'})
            order_id = payment['id']
            
            context = {
                'cartItems' : cartItems,
                'order' : order,
                'total': total,
                'discount_amount': discount_amount,
                'grandTotal': grandTotal,
                'razorpayTotal' : razorpayTotal,
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

            
            return render(request, 'payment.html', context)
    else:
        return redirect('checkout')            


@login_required(login_url='login')
def orderCompleted(request):
    cartItems = CartItem.objects.filter(user=request.user, isActive=True)
    total = utils.total(cartItems) or 0
    quantity = utils.quantity(cartItems) or 0
    tax = utils.tax(total) or 0
    grandTotal = total + tax

    order_number = request.session.get('order_number', None)
    print('order_number',order_number)
    order = Order.objects.filter(orderNumber=order_number, user = request.user)
    # order = Order()
    # order.status = 'Completed'
    # order.isOrdered = True
    # order.orderTotal = grandTotal
    # order.user = request.user
    # order.save()
    # print(order)
    
    # payment_data = json.loads(request.COOKIES.get('payment_data', '{}'))
    # # storing payment data
    # payment = Payment(
    #     user = request.user,
    #     paymentMethod = payment_data.get('Cash on Delivery'),
    #     paymentId = payment_data.get('payment_id'),
    #     amountPaid = payment_data.get('amount_paid'),
    # )
    # # move the cart items to the order product table

    # # Reduce the quantity in the stock

    # # Clear Cart
    # cartItems = CartItem.objects.filter(user = request.user)
    # for item in cartItems:
    #     orderProduct = OrderProduct()
    #     orderProduct.order_id = order_number
    #     orderProduct.user = request.user
    #     # orderProduct.product_id = item.product.id
    #     orderProduct.ordered = True
    #     # orderProduct.quantity =item.quantity
    #     # orderProduct.productPrice = item.product.price

    #     orderProduct.save()



# ==================================================================================
 # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
       
        paymentMethod = 'COD',
        paymentId = 'COD Order',
        amountPaid = grandTotal,
        status ='Successful',
    )
    payment.save()



    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        # orderproduct.order = order.
        # orderproduct.payment = payment
        orderproduct.user_id = request.user
        # orderproduct.product_id = item.product_id
        # orderproduct.quantity = item.quantity
        # orderproduct.productPrice = item.product.price
        # orderproduct.ordered = True
        # orderproduct.save()

        # cart_item = CartItem.objects.get(id=item.id)
        # productVariation = cart_item.variations.all()
        # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        # orderproduct.variations.set(productVariation)
        # orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()


    order = Order.objects.get(user=request.user,  orderNumber = order_number)

    context = {
        'order_number': order_number,
        'order': order,
        'cartItems': cartItems,
        'grandTotal' : grandTotal,
        'order' : order,
            }
    
    return render(request, 'orderCompleted.html', context)

@login_required(login_url='login')
def razorpayCheck(request):
    if request.method == "POST":
        paymentOrder = Payment()
        paymentOrder.user = request.user
        paymentOrder.paymentMethod = request.POST.get('paymentMode')
        if request.POST.get('payment_id'):
            paymentOrder.payment_id = request.POST.get('payment_id')
        paymentOrder.amount_paid = request.POST.get('grand_total')
        paymentOrder.status = True
        # paymentOrder.status=request.POST.get('status')
        paymentOrder.save()
        print("payment is saved")

        order_number = request.POST.get('order_no')
        order = Order.objects.get(user=request.user, order_number=order_number)
        order.payment = paymentOrder
        order.is_ordered = True
        order.status = 'Processing'
        print("Grand total", request.POST.get('grand_total'))
        order.order_total = request.POST.get('grand_total')
        print(order.order_total)
        order.save()
         

        # moving the order details into order product table

        cart_items = CartItem.objects.filter(user=request.user)
        print(cart_items,"hi")
        
        for cart_item in cart_items:
            order_product = OrderProduct()
            order_product.order = order
            order_product.payment = paymentOrder
            order_product.user = request.user
            order_product.product = cart_item.product
            order_product.quantity = cart_item.quantity
            order_product.product_price = cart_item.product.price
            order_product.ordered = True
            order_product.save()
            item = CartItem.objects.get(id=cart_item.id)
            product_variation = item.variations.all()
            order_product = OrderProduct.objects.get(id=order_product.id)
            order_product.variations.set(product_variation)
            order_product.save()

            # reducing the quantity of product after selling it
            product = Product.objects.get(id=cart_item.product_id)
            product.stock -= cart_item.quantity
            product.save()

        # deleting the cart itemszzzzzzzzzzzzzzz
        CartItem.objects.filter(user=request.user).delete()

        # send order number and transaction id

        data = {
            'order_number': order_number,
            'tansID': paymentOrder.payment_id,
        }
        print("completed")
        # return render(request,'orders/order_completed.html')
        # return JsonResponse({'status': 'Your order placed successfully!','data':data})
        return redirect('orderCompleted')

@login_required(login_url='login')
def orderCompletedAjax(request):
    print('inside Order completed ajax')
    cartItems = CartItem.objects.filter(user=request.user, isActive=True)
   
    total = utils.total(cart_items)
    quantity = utils.quantity(cart_items)
    tax = utils.tax(total)
    grandTotal = total + tax

    order_number = request.session.get('order_number', None)
    order = Order.objects.get(user=request.user, isOrdered = False, orderNumber = order_number)
    order.status = 'Completed'
    print(order)
    
    # payment_data = json.loads(request.session.pop('payment_data', '{}'))
    payment_data = json.loads(request.COOKIES.get('payment_data', '{}'))
    test_string = request.session.pop('test_string', 'default_value')
    print(test_string) 

    print(payment_data)
    context = {'order_number': order_number, 'payment_data' : payment_data, 'order': order,}
    
    context = {
    'order_number': order_number,
    'order': order,
    'cartItems': cartItems,
    'grandTotal' : grandTotal,
    'order' : order,
            }
# ==================================================================================
 # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        paymentId = 'Rz_pay_qw234',
        paymentMethod = 'Razorpay',
        amountPaid = grandTotal,
        status ='Successful',
    )
    payment.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        # orderproduct = OrderProduct()
        # # orderproduct.order = order.Id
        # orderproduct.Payment = payment
        # orderproduct.user= request.user
        # orderproduct.quantity = item.quantity   
        # orderproduct.productPrice = item.product.price
        # orderproduct.ordered = True
        # orderproduct.save() 

        # cart_item = CartItem.objects.get(id=item.id)
        # product_variation = cart_item.variations.all()
        # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        # orderproduct.variations.set(product_variation)
        # orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()
    return render(request, 'orderCompleted.html', context)


# NEW Payment trial
# client = razorpay.Client(auth=(ecommerce.settings.RAZORPAY_KEY_ID, ecommerce.settings.RAZOR_KEY_SECRET))
# print(client)
# def create_order(request):
#     currentUser = request.user
#     cartItems = CartItem.objects.filter(user = currentUser)
#     cartCount = cartItems.count()
#     if cartCount <=0:
#         return redirect('home') 
    
 
#     total = utils.total(cartItems)
#     request.session['order_total'] = total

#     payment_data = {
#             'amount': int(total * 100),
#             'currency': 'INR',
#             'payment_capture': '1',
#         }
#     payment = client.order.create(data=payment_data)
#     return render(request, 'payment.html')

@csrf_exempt
def razorpay_payment(request):
    grandTotal = request.session.get('grand_total', None)
    if request.method == 'POST':
        amount = grandTotal
        client = razorpay.Client(auth=(ecommerce.settings.RAZOR_KEY_ID, ecommerce.settings.RAZOR_KEY_SECRET))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, 'payment.html', {'payment': payment})
    return redirect('cart')


@csrf_exempt
def razorpay_payment_success(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST['razorpay_payment_id']
        razorpay_order_id = request.POST['razorpay_order_id']
        razorpay_signature = request.POST['razorpay_signature']
        client = razorpay.Client(auth=(ecommerce.settings.RAZOR_KEY_ID, ecommerce.settings.RAZOR_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature
            })
            # Payment success
            return render(request, 'orders/payment_success.html')
        except:
            # Payment failed
            return render(request, 'orders/payment_failed.html')
    return redirect('cart')