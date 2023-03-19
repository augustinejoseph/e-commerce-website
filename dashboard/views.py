
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


def returnProduct(request, order_id):
    user = Account.objects.get(id = request.user.id)
    order = Order.objects.get(id = order_id)
    if order.status == 'Delivered':
        order.status = "Refunded"
        order.save()
        user.wallet += order.orderTotal
        user.save()
        messages.success(request, 'Return Succcessful. Amound added to the wallet')
        return redirect('orders')
    else:
        messages.error(request, 'Unable to return, Contact Admin for more details')
        return redirect('orders')

