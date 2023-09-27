import sys
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from orders.models import OrderProduct
from products.models import Product, ReviewRating, Variations
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# filter the product
from products.filters import ProductFilter
import django_filters
from django.views.generic.list import ListView


class ProductListView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 8
    productsCount = 0

    def get_queryset(self):
        queryset = super().get_queryset()
        brand = self.request.GET.get("brand")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        category_slug = self.kwargs.get("categorySlug")

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if brand:
            queryset = queryset.filter(brand=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        queryset = queryset.filter(isAvailable=True)

        return queryset


def productDetails(request, categorySlug, productSlug):
    singleProduct = Product.objects.get(category__slug=categorySlug, slug=productSlug)
    variations = Variations.objects.all()
    reviews = ReviewRating.objects.filter(product_id=singleProduct.id, status=True)

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product_id=singleProduct.id
            ).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product_id=singleProduct.id, status=True)

    context = {
        "singleProduct": singleProduct,
        "variations": variations,
        "reviews": reviews,
        "orderproduct": orderproduct,
    }

    return render(request, "productDetails.html", context)


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        products = Product.objects.order_by("createdDate").filter(
            Q(productDescription__icontains=keyword)
            | Q(productName__icontains=keyword),
            isAvailable=True,
        )
        context = {"products": products}

    return render(request, "home.html", context)
