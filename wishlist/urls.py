from django.urls import path
from .views import WishlistListView
# from .views import  AddToWishlist
from . import views
from cart.views import addCart


urlpatterns = [
    path('', WishlistListView.as_view(), name = 'wishlist'),
    # path ('add/', WiishlistListCreateView.as_view(), name = 'wishkistCreate'),
    # path('addWishlist/<int:productId>/', AddToWishlist.as_view(), name='addWishlist'),
    path('addWishlist/<int:productId>/', views.addWishlist, name ='addWishlist'),
    path('removeWishlist/<int:productId>/', views.removeWishlist, name ='removeWishlist'),
    path('addcart/<int:productId>/', views.addCart, name = 'addcart'),

]
