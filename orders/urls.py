from django.urls import path
from . import views
urlpatterns = [
    path('place_order/', views.placeOrder , name = 'placeOrder'),
    path('payments/', views.payments, name = 'payments'),
    # path('orderSuccess/', views.orderSuccess, name = 'orderSuccess'),
    path('order-completed/', views.orderCompleted, name="orderCompleted"),
    path('proceed-to-pay/',views.razorpayCheck, name='razorpayCheck'),


    
    path('order-completed-ajax/', views.orderCompletedAjax, name="orderCompletedAjax"),


     
]
