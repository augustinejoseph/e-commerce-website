from django import forms
from .models import Wishlist

class AddToWishlistForm(forms.ModelForm):
    class Meta:
        model  = Wishlist
        fields = []