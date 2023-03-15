"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import ProductListView

urlpatterns = [
   
    # path('', views.home, name='home'),
    path('accounts/',include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('customAdmin/', include('customAdmin.urls')),
    path('pages/', include('pages.urls')),
    path('dashboard/', include('dashboard.urls')),
    # path('category/<slug:categorySlug>/', views.home, name = 'productByCategory'),
    # path('category/<slug:categorySlug>/<slug:productSlug>/', views.productDetails, name = 'ProductDetails'),
    path('search/', views.search, name = 'search'),
    
    path('category/<slug:categorySlug>/', ProductListView.as_view(), name='productByCategory'),
    path('category/<slug:categorySlug>/<slug:productSlug>/', views.productDetails, name='ProductDetails'),

    
    path('', views.ProductListView.as_view(), name='home'),

    # Orders
    path('orders/', include('orders.urls')),
    path('wishlist/', include('wishlist.urls')),

    # Admin Panel
    path('admin/', admin.site.urls),
    # path('adminpanel/', include('adminPanel.urls', namespace='adminPanel')),
    path('adminpanel/', include('adminPanel.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
