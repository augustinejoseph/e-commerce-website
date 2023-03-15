
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from accounts.models import Account,UserProfile,User
from dashboard.models import Account
from dashboard.forms import UserForm,UserProfile,UserProfileForm
from orders.models import Order


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

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


# def edit(request):
#     useraddress = Address.objects.all().filter(user=request.user).first()
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         address_form = UserAddressForm(request.POST, instance=useraddress)
#         if user_form.is_valid() and address_form.is_valid():
#             user_form.save()
#             address_form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('edit_profile')
#         # else:
#         #     context={'error':user_form.errors,

#         #             'error2':address_form.errors
            
#         #     }
#         #     return render(request, 'profile.html', context)
#     else:
#          user_form = UserForm(instance=request.user)
#          address_form = UserAddressForm(instance=useraddress)
#          context = {
#                 'user_form': user_form,
#                 'address_form': address_form
#             }
#         #  full_name = str(user.first_name) + str(user.last_name)   
#     return render(request, 'customers/edit_profile.html', context)



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



@login_required
def address(request):
    userProfile = UserProfile.objects.get(user = request.user)


    context={
        'profile_form' : userProfile,
        
    }
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
        return redirect('dashboard')
    else:
        messages.error(request, 'Unable to return, Contact Admin for more details')
        return redirect('dashboard')



# =================================================CBV=========================================================================
# from django.shortcuts import render
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import UpdateView
# from django.urls import reverse_lazy

# from accounts.models import Account

# class UserProfileView(LoginRequiredMixin, DetailView):
#     model = Account
#     template_name = 'dashboard.html'


#     def get_object(self):
#         return self.request.user.account

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.email
#         return context
    

# class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model               = Account
#     fields              = ['first_name', 'last_name', 'email']
#     template_name       = 'edit.html'
#     success_url         = 'dashboard'

#     def get_object(self):
#         return self.request.Account


