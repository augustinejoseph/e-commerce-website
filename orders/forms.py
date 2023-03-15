from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['firstName', 'lastName', 'email', 'phone', 'addressLineOne',  'city', 'state']
    

