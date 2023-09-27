from . import views
from django.urls import path
from .views import CartView, CheckoutView, get_address
from . import views


urlpatterns = [
    path("addcart/<int:productId>/", views.addCart, name="addCart"),
    path(
        "removeCartItem/<int:productId>/<int:cartItemId>/",
        views.removeCartItem,
        name="removeCartItem",
    ),
    path(
        "removeCart/<int:productId>/<int:cartItemId>/",
        views.removeCart,
        name="removeCart",
    ),
    path("", CartView.as_view(), name="cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("get_address/<int:address_id>/", get_address, name="get_address"),
]
