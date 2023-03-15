from django.contrib import admin
from .models import Order, OrderProduct ,Payment

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amountPaid','status', 'createdAt', 'paymentMethod']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'orderNumber', 'dateCreated', 'firstName', 'lastName','dateCreated',  'orderTotal', 'status', 'isOrdered', 'email', 'phone']
    list_editable = ['status', 'isOrdered']
    # list_filter = ['user', 'firstName', 'dateCreated', 'email', 'phone', 'orderTotal']
    list_per_page=15

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'Payment','user', 'product', 'quantity', 'ordered',]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment, PaymentAdmin)