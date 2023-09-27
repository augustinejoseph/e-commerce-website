from django.urls import path
from .views import WishlistListView
from . import views
from cart.views import addCart


urlpatterns = [
    path("", WishlistListView.as_view(), name="wishlist"),
    path("addWishlist/<int:productId>/", views.addWishlist, name="addWishlist"),
    path(
        "removeWishlist/<int:productId>/", views.removeWishlist, name="removeWishlist"
    ),
    path("addcart/<int:productId>/", views.addCart, name="addcart"),
]
