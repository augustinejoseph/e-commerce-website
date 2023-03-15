from django.contrib import admin
from .models import Cart, CartItem,Coupon, UserCoupon

# Register your models here.

class cartAdmin(admin.ModelAdmin):
    list_display = ( 'cartId', 'dateAdded')

class cartItemAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'product', 'cart', 'quantity',  'isActive')

class couponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'expiry')

class UserCouponAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon']

admin.site.register(Cart, cartAdmin)
admin.site.register(CartItem, cartItemAdmin)
admin.site.register(Coupon, couponAdmin)
admin.site.register(UserCoupon, UserCouponAdmin)