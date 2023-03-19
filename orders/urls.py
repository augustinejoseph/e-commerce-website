from django.urls import path
from . import views
urlpatterns = [
    # path('place_order/', views.placeOrder , name = 'placeOrder'),
    path('payment/', views.payment, name = 'payment'),
    # path('order-completed/', views.orderCompleted, name="orderCompleted"),
    # path('proceed-to-pay/',views.razorpayCheck, name='razorpayCheck'),
    # path('order-completed-ajax/', views.orderCompletedAjax, name="orderCompletedAjax"),

    # New Payment
    path('razorpay-payment/', views.razorpay_payment, name='razorpay_payment'),
    # path('razorpay-payment-success/', views.razorpay_payment_success, name='razorpay_payment_success'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),

     
]
