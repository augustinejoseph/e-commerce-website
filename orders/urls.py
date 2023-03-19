from django.urls import path
from . import views
urlpatterns = [
    path('payment/', views.payment, name = 'payment'),
    path('razorpay-payment/', views.razorpay_payment, name='razorpay_payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('cod/', views.cod, name = 'cod'),

     
]
