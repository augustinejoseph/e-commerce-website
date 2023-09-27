from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import ProductListView

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("cart/", include("cart.urls")),
    path("pages/", include("pages.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("search/", views.search, name="search"),
    path(
        "category/<slug:categorySlug>/",
        ProductListView.as_view(),
        name="productByCategory",
    ),
    path(
        "category/<slug:categorySlug>/<slug:productSlug>/",
        views.productDetails,
        name="ProductDetails",
    ),
    path("", views.ProductListView.as_view(), name="home"),
    # Orders
    path("orders/", include("orders.urls")),
    path("wishlist/", include("wishlist.urls")),
    # Admin Panel
    path("admin/", admin.site.urls),
    path("adminpanel/", include("adminPanel.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
