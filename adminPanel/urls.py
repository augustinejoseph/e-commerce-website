from django.urls import path
from . import views
from .views import (
    UserListView,
    ProductListView,
    CategoryListView,
    OrderListView,
    EditProduct,
    EditCategory,
    EditUser,
    user_details,
    UserCreateView,
    CategoryCreateView,
    OrderUpdateView,
    OrderDetailView,
    ProductCreateView,
    AdminDashboard,
)


# app_name = 'adminPanel'
urlpatterns = [
    # path('', views.adminDashboard, name='admindashboard'),
    path("", AdminDashboard.as_view(), name="admindashboard"),
    path("adminlogin/", views.adminLogin, name="adminLogin"),
    path("logout/", views.adminLogout, name="adminLogout"),
    path("sales-chart/", views.sales_chart, name="sales_chart"),
    # User Management
    path("user/", UserListView.as_view(), name="user_list"),
    path("users/<int:user_id>/", user_details, name="user_details"),
    path("user-search/", views.UserSearch, name="user_search"),
    path("edit-user/<int:pk>/", EditUser.as_view(), name="edit_user"),
    path("delete-user/<int:pk>/", views.deleteUser, name="delete_user"),
    path("create-user/", UserCreateView.as_view(), name="user_create"),
    # Category Management
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category-search/", views.CategorySearch, name="category_search"),
    path("edit-category/<int:pk>/", EditCategory.as_view(), name="edit_category"),
    path("create-category/", CategoryCreateView.as_view(), name="category_create"),
    path("delete-category/<int:pk>/", views.deleteCategory, name="delete_category"),
    path("disable-category/<int:pk>/", views.disableCategory, name="disable_category"),
    # Product
    path("product/", ProductListView.as_view(), name="product_list"),
    path("product-search/", views.ProductSearch, name="product_search"),
    # path('edit-product/<int:product_id>', views.editProduct, name="edit_product"),
    path("edit-product/<int:pk>/", EditProduct.as_view(), name="edit_product"),
    path("delete-product/<int:pk>/", views.deleteProduct, name="delete_product"),
    path("create-product/", ProductCreateView.as_view(), name="create_product"),
    # Order Management
    path("order/", OrderListView.as_view(), name="order_list"),
    path("order-search/", views.OrderSearch, name="order_search"),
    path("edit-order/<int:pk>/", OrderUpdateView.as_view(), name="edit_order"),
    path("oder-detail/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("delete-order/<int:pk>/", views.deleteOrder, name="delete_order"),
]
