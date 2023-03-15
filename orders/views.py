import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from cart.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from products.models import Product
import datetime
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from cart import utils

@login_required(login_url='login')
def placeOrder(request):
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
    razorpayTotal = grandTotal*100

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
            data.isOrdered = True
            #data.country = form.cleaned_data['country']
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
                }
            print(order)
            print(cartItems)

            return render(request, 'reviewOrder.html', context)
    else:
        return redirect('checkout')            
 
@login_required(login_url='login')
def payments(request):
    pass 

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
        print('order status updated============================')
        print("Grand total", request.POST.get('grand_total'))
        order.order_total = request.POST.get('grand_total')
        print(order.order_total)

        print('order total are updated ============================')
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