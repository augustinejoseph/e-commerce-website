from django.urls import path
from . import views
from dashboard.views import Addaddress

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('view/', views.dashboard, name = 'dashboard'),
    path('edit/', views.edit, name='edit'),
    path('orders/', views.orders, name='orders'),
    path('change_password/', views.changePassword, name='changePassword'),
    path('address/', views.address, name = 'address'),
    path('add-funds/', views.add_funds, name='add_funds'),
    path('return-product/<int:order_id>/', views.returnProduct, name = "returnProduct"),
    path('add-address/' , Addaddress.as_view(), name = 'addAddress'),
    path('order-details/<int:order_id>/', views.orderDetails, name = 'orderDetails'),
    path('cancel-order/<int:order_id>/', views.cancelOrder, name ='cancelOrder'),

]








# ===================================================CBV================================================================


# from django.urls import path
# from .views import UserProfileView, UserProfileUpdateView

# urlpatterns = [
#     path('', UserProfileView.as_view(), name = 'dashboard'),
#     path('edit/', UserProfileUpdateView.as_view(), name = 'dashboardUpdate')
# ]

