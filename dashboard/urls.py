from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('view/', views.dashboard, name = 'dashboard'),
    path('edit/', views.edit, name='edit'),
    path('orders/', views.orders, name='orders'),
    path('change_password/', views.changePassword, name='changePassword'),
    path('address/', views.address, name = 'address'),
    path('add-funds/', views.add_funds, name='add_funds'),
    path('return-roduct/<int:order_id>/', views.returnProduct, name = "returnProduct"),

]








# ===================================================CBV================================================================


# from django.urls import path
# from .views import UserProfileView, UserProfileUpdateView

# urlpatterns = [
#     path('', UserProfileView.as_view(), name = 'dashboard'),
#     path('edit/', UserProfileUpdateView.as_view(), name = 'dashboardUpdate')
# ]

