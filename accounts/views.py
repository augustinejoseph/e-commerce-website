from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.core.cache import cache

# Email Imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from products.models import Product

# Cart Imports
from cart.models import Cart, CartItem
from cart.views import _cartId


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.save()

            # user activation through email
            current_site = get_current_site(request)
            mail_subject = "Click on the following link to activate your Account"
            message = render_to_string(
                "account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect("/accounts/login?command=verification&email=" + email)
    else:
        form = RegistrationForm
    context = {
        "form": form,
    }
    return render(request, "register.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cartId=_cartId(request))
                isCartItemExists = CartItem.objects.filter(cart=cart).exists()
                if isCartItemExists:
                    cartItem = CartItem.objects.filter(cart=cart)

                    for item in cartItem:
                        item.user = user
                        item.save()

            except:
                pass
            auth.login(request, user)
            request.session["email"] = email
            messages.success(request, "You have successfully logged in")
            return redirect("home")
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect("login")

    return render(request, "login.html")


@login_required(login_url="home")
@never_cache
def logoutUser(request):
    logout(request)
    request.session.flush()
    cache.clear()
    messages.success(request, "You have successfully logged out")
    return redirect("home")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is now activated")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation LInk")
        return redirect("register")


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # sending the email for password reset
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string(
                "reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, "Email send Successfully. Check email for furher instructions"
            )
            return redirect("login")
        else:
            messages.error(request, "Account does not exists")
            return redirect("forgotPassword")

    return render(request, "forgotPassword.html")


def resetpasswordValidate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password")
        return redirect("resetPassword")
    else:
        messages.error(request, "Link has been expired")
        return redirect("login")


def resetPassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset Success")
            return redirect("login")

        else:
            messages.error(request, "Passwords does not match")
            return redirect("resetPassword")

    else:
        return render(request, "resetPassword.html")
