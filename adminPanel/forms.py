from django import forms
from products.models import Product
from category.models import Category
from accounts.models import Account


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "productName",
            "brand",
            "productDescription",
            "slug",
            "images",
            "price",
            "isAvailable",
            "stock",
            "category",
        ]
        widgets = {
            "slug": forms.TextInput(attrs={"readonly": True}),
            "productName": forms.TextInput(attrs={"id": "id_productName"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["categoryName", "slug"]
        widgets = {
            "slug": forms.TextInput(attrs={"readonly": True}),
            "categoryName": forms.TextInput(attrs={"id": "id_categoryName"}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["readonly"] = True
