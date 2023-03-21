
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from accounts.models import Account,UserProfile,User
from dashboard.models import Account
from dashboard.forms import UserForm,UserProfile,UserProfileForm
from orders.models import Order, OrderProduct
from dashboard.forms import AddressForm
from django.views.generic.edit import FormView
import razorpay
import ecommerce.settings 

# Shipping Addresses
class Addaddress(FormView):
    form_class = AddressForm
    template_name = 'addAddress.html' 
    success_url = '/dashboard/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def orderDetails(request, order_id):
    order = Order.objects.get(id = order_id)
    orderProduct = OrderProduct.objects.filter(order_id = order)
    print('------------',order )
    print('------------',orderProduct)
    context= {
        'order' : order,
        'orderProduct' : orderProduct
        }
    return render(request, 'orderDetails.html', context)

@login_required
def cancelOrder(request, order_id):
    order = Order.objects.get(id = order_id)
    order.status = 'Cancelled'
    order.save()
    return redirect('orders')

@login_required
def edit(request):
    print(request.user)
    userProfile = get_object_or_404(UserProfile, user = request.user)
    if request.method == 'POST':
        userForm = UserForm(request.POST, instance=request.user)
        profileForm = UserProfileForm(request.POST, request.FILES,instance=userProfile)
        if userForm.is_valid() and profileForm.is_valid:
            userForm.save()
            profileForm.save()
            messages.success(request, 'Your Profile Has Been Updated')
            return redirect('edit')
    else:
        userForm = UserForm(instance=request.user)
        profileForm = UserProfileForm(instance = userProfile)

        context = {
            'user_form' : userForm,
            'profile_form' : profileForm,
            'userProfile' : userProfile
        }
    return render(request,'editProfile.html', context)


@login_required
def orders(request):
    orders = Order.objects.filter(user = request.user, isOrdered=True).order_by('-dateCreated')
    context = {
        'orders' : orders
        }
    print(orders)
    return render(request, 'orders.html', context)

@login_required
def changePassword(request):
    user = Account.objects.get(username__exact = request.user.username)
    if request.method == 'POST':
        currentPassword = request.POST['currentPassword']
        newPassword = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if confirmPassword == newPassword:
            success = user.check_password(currentPassword)
            if success:
                user.set_password(newPassword)
                user.save()
                messages.success(request, 'Password Changed Successfully')
            else:
                messages.error(request, 'Passwords does not match. Try again')
                return redirect('changePassword')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request , 'changePassword.html')
    return render(request, 'changePassword.html')


# Users Address
@login_required
def address(request):
    userProfile = UserProfile.objects.get(user = request.user)
    context={'profile_form' : userProfile,}
    return render(request, 'address.html', context)

def add_funds(request):
    if request.method == "POST":
        amount = request.POST['amount']
        amount = float(amount)
        try:
            if amount <= 0:
                messages.error(request, 'Invalid amount, Enter an amount above 1')
                pass
                return redirect('dashboard')
            else:
                account  = Account.objects.get(id = request.user.id)
                account.wallet += amount
                account.save()
                messages.success(request, "Amount added Successfully")
                return redirect('dashboard')
        except ValueError as e:
            messages.error(request, str(e))

# #Old one with wallet
# def returnProduct(request, order_id):
#     user = Account.objects.get(id = request.user.id)
#     order = Order.objects.get(id = order_id)
#     if order.status == 'Delivered':
#         order.status = "Refunded"
#         order.save()
#         user.wallet += order.orderTotal
#         user.save()
#         messages.success(request, 'Return Succcessful. Amound added to the wallet')
#         return redirect('orders')
#     else:
#         messages.error(request, 'Unable to return, Contact Admin for more details')
#         return redirect('orders')


# client = razorpay.Client(auth=(ecommerce.settings.RAZOR_KEY_ID, ecommerce.settings.RAZOR_KEY_SECRET))
# @login_required
# def returnProduct(request, order_id):
#     # Fetch order details from database
#     order = Order.objects.get(id=order_id)

#     # Check if the order belongs to the logged-in user
#     if order.user != request.user:
#         messages.error(request, 'You are not authorized to access this order.')
#         return redirect('dashboard')

#     # Check if the order has already been refunded
#     if order.status == 'Refunded':
#         messages.error(request, 'This order has already been refunded.')
#         return redirect('dashboard')

#     # Initiate refund on Razorpay
#     refund_amount = order.orderTotal* 100 # Convert to paise
#     try:
#         refund_data = {
#             "payment_id": order.payment_id,
#             "amount": refund_amount,
#             "speedy_complete": True
#         }
#         refund = client.payment.refund.create(**refund_data)

#         # Update order details in database
#         order.status = 'Refunded'
#         print('------------order status after refund', order.status)
#         order.refund_id = refund['id']
#         print('------------ refund id after refund', order.refund)
#         order.save()

#         messages.success(request, 'Refund initiated successfully.')
#     except Exception as e:
#         messages.error(request, 'Failed to initiate refund: ' + str(e))

#     return redirect('dashboard')

client = razorpay.Client(auth=(ecommerce.settings.RAZOR_KEY_ID, ecommerce.settings.RAZOR_KEY_SECRET))
@login_required
def returnProduct(request, order_id):
    # Fetch order details from database
    order = Order.objects.get(id=order_id)
    paymentId = order.payment
    # Check if the order belongs to the logged-in user
    if order.user != request.user:
        messages.error(request, 'You are not authorized to access this order.')
        return redirect('dashboard')

    # Check if the order has already been refunded
    if order.status == 'Refunded':
        messages.error(request, 'This order has already been refunded.')
        return redirect('dashboard')

    # Initiate refund on Razorpay
    refund_amount = order.orderTotal*100
    paymentMethod = order.payment.paymentMethod
    print('-------------paymentMethod ', paymentMethod)
    if paymentMethod == 'Razorpay':
        try:
            client.payment.refund(paymentId,{
                "amount": refund_amount,
                "speed": "optimum",
                "receipt": order.orderNumber
                })
            # Update order details in database
            order.status = 'Refunded'
            print('------------order status after refund', order.status)
            order.save()

            messages.success(request, 'Refund initiated successfully.')
        except Exception as e:
            messages.error(request, 'Failed to initiate refund: ' + str(e))
    else:
        if order.status == 'Delivered':
            order.status = "Refunded"
            order.save()
            messages.success(request, 'Request Processed.')
        if order.status == 'New':
            order.status = "Cancelled"
            order.save()
            messages.success(request, 'Order cancelled successfully.')

    return redirect('dashboard')