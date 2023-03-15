from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from accounts.forms import RegistrationForm
from django.views.decorators.cache import never_cache
from django.contrib import messages, auth



# Create your views here.
def admin(request):
    context = {}
    return render(request, 'adminpanel.html', context)

def adminLogin(request):
    # if 'username' in request.session:
    #     return redirect('admin_dashboard')
    # context = {}

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email , password=password)

        if user is not None:
            if user.is_superadmin:
                return redirect('admin_dashboard')
            else:
                messages.info(request, 'Access Denied, You don\'t have admin privilages')
        else:
            messages.info(request, 'Username or password is Incorrect')
    return render(request, 'customadmin_login.html')


    # return render(request, 'customadmin_login.html')
    # 
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)

        if user is not None:
            login(request,user)
            request.session['username'] = username
            if user.is_superadmin:
                return redirect('admin_dashboard')
            else:
                messages.info(request, 'Access Denied, You don\'t have admin privilages')
        else:
            messages.info(request, 'Username or password is Incorrect')
    return render(request, 'customAdmin/customadmin_login.html', context)

@never_cache
@user_passes_test(lambda u: u.is_superadmin)
def dashboard(request):
    if 'username' in request.session:
        context = {
            'users': User.objects.all()
        }
        return render(request, 'customAdmin/admin_dashboard.html', context)
    else:
        return redirect('admin_login')

@user_passes_test(lambda u: u.is_superadmin)
def searchUser(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        user = User.objects.filter(username__icontains = searched)
        context={
        'searched' : searched,
         'user' : user,
        }
        return render(request, 'customAdmin/searchUser.html', context)
    else:
        return render(request, 'customAdmin/searchUser.html')

@user_passes_test(lambda u: u.is_superadmin)
def createUser(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('admin_dashboard')
    return render(request, 'customAdmin/createUser.html', {'form' : form, 'title': 'Submit'})

@user_passes_test(lambda u: u.is_superadmin)
def updateUser(request,id):
    user=User.objects.get(pk=id)
    form = RegistrationForm(instance = user)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Details Updated Successfully')
            return redirect('admin_dashboard')
    return render(request, 'customAdmin/createUser.html', {'form': form})

@user_passes_test(lambda u: u.is_superadmin)
def deleteUser(request, id):
    user=User.objects.get(pk=id)
    if request.method == 'POST':
        if user.is_superadmin:
            pass
        else:
            user.delete()
        return redirect('admin_dashboard')
    context = { 'user': user}
    return render(request, 'customAdmin/deletePage.html', context)

@user_passes_test(lambda u: u.is_superadmin)
def adminLogout(request):
    logout(request)
    if 'username' in request.session:
        request.session.flush()
    return redirect('admin_login')




def test(request):
    context={
        'test' : 'test'
    }
    return render(request, 'app/test.html', context)



