from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from products.models import Product
from category.models import Category
from accounts.models import Account
from orders.models import Order, OrderProduct
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib import auth, messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CategoryForm, UserForm
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from django.db.models.functions import TruncDay



from django.contrib.auth import login

def adminLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None and user.is_superadmin:
            login(request, user)  # <-- use the login() function to authenticate the user
            messages.success(request, 'Login successful')
            return redirect('admindashboard')
        else:
            messages.error(request, 'Permission Denied')
            return redirect('adminLogin')

    return render(request, 'adminLogin.html')

@never_cache   
def adminLogout(request):
    logout(request)
    request.session.flush()
    messages.success(request,'Logged out Successfully')
    return redirect('adminLogin')



class AdminDashboard(LoginRequiredMixin, TemplateView):
    template_name ='adminDashboard.html'
    login_url =reverse_lazy('adminLogin')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the sales data for the last 7 days
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        sales_data = OrderProduct.objects.filter(createdAt__range=(start_date, end_date)).annotate(day=TruncDay('createdAt')).values('day').annotate(total_sales=Sum('productPrice'))
        print(end_date)
        print(start_date)
        print(sales_data)
        # Add the sales data to the context dictionary
        context['sales_data'] = sales_data
        return context
    
        
# ====================================================USER================================================================
# User lIst view

class UserListView(LoginRequiredMixin, ListView):
    login_url =reverse_lazy('adminLogin')
    model = Account
    template_name = 'userList.html'
    context_object_name = 'users'
    paginate_by = 10
    
def user_details(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    data = {
        'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            # add more fields here as needed
        }
    }
    return JsonResponse(data)

# Delete the user
def deleteUser(request, pk):
    user = Account.objects.get(id = pk)
    if not user.is_active:
        user.is_active = True
        messages.success(request, 'User is now active')
    else:
        user.is_active = False
        messages.error(request, 'User is now Inactive')
    user.save()
    return redirect('user_list')


#User search functionality

def UserSearch(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        users = Account.objects.filter(Q(first_name__icontains = keyword) | Q(last_name__icontains = keyword)  | Q(email__icontains = keyword) | Q(phone_number__icontains = keyword))
    return render(request, 'userList.html', {'users':users})

class EditUser(UpdateView):
    login_url =reverse_lazy('adminLogin')
    model = Account
    template_name = 'editUser.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')

# Add user
class UserCreateView(LoginRequiredMixin,CreateView):
    login_url =reverse_lazy('adminLogin')
    model = Account
    fields = ['first_name', 'last_name','username', 'email', 'phone_number','is_admin', 'is_active']
    template_name = "createUser.html"
    success_url = reverse_lazy("user_list")

# ====================================================PRODUCT================================================================

# Product list view
class ProductListView(LoginRequiredMixin, ListView):
    login_url =reverse_lazy('adminLogin')
    model = Product
    template_name = 'productList.html'
    context_object_name = 'products'
    paginate_by = 5

#Product search functionality
def ProductSearch(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        products = Product.objects.order_by('createdDate').filter(Q(productDescription__icontains = keyword) | Q(productName__icontains = keyword))
    return render(request, 'productList.html', {'products':products})

# Edit Product
class EditProduct(LoginRequiredMixin,UpdateView):
    login_url =reverse_lazy('adminLogin')
    model = Product
    form_class = ProductForm
    template_name = 'editProduct.html'
    success_url = reverse_lazy('product_list')

# Create Product
class ProductCreateView(CreateView):
    login_url =reverse_lazy('adminLogin')
    model = Product
    template_name = 'createProduct.html'
    success_url = reverse_lazy('product_list')
    fields = '__all__'
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Product created successfully!')
        return response
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'There was an error creating the product. Please try again.')
        return response
    
# Delete Product
def deleteProduct(request, pk):
    product = Product.objects.get(id = pk)
    if product.isAvailable  is True:
        product.isAvailable = False
        messages.success(request, 'Product is not available from now')
    else:
        product.isAvailable = True
        messages.success(request, "Product is available from now")
    product.save()
    return redirect('product_list')


# ====================================================CATEGORY================================================================
# Category lIst view
class CategoryListView(LoginRequiredMixin,ListView):
    login_url =reverse_lazy('adminLogin')
    model = Category
    template_name = 'categoryList.html'
    context_object_name = 'categories'
    template_name = 'categoryList.html'
    paginate_by = 5

# Create New Cadtegory
class CategoryCreateView(LoginRequiredMixin, CreateView):
    login_url =reverse_lazy('adminLogin')
    model = Category
    fields = ['categoryName','slug']
    template_name = 'createCategory.html'
    success_url = reverse_lazy('category_list')
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['slug'].widget.attrs['readonly'] = True
        return form

#Category search functionality
def CategorySearch(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        categories = Category.objects.filter(Q(categoryName__icontains = keyword) | Q(slug__icontains = keyword))
        print(categories)
    return render(request, 'categoryList.html', {'categories':categories})

# Edit Category
class EditCategory(LoginRequiredMixin, UpdateView):
    login_url =reverse_lazy('adminLogin')
    model = Category
    form_class = CategoryForm
    template_name = 'editCategory.html' 
    success_url = reverse_lazy('category_list')

# Disable Category
def disableCategory(request, pk):
    category = Category.objects.get(id=pk)
    print('qwertyuiopqwertyuio category')
    if not category.isActive:
        category.isActive = True
        messages.success(request, "Category is enabled")
        print('qwertyuiopqwertyuio category Falsed')
    else:
        category.isActive = False
        messages.error(request, "Category is disabled")
        print('qwertyuiopqwertyuio category Trued')
    category.save()
    return redirect('category_list')

# Delete Category
def deleteCategory(request, pk):
    category = Category.objects.get(id = pk)
    products = Product.objects.filter(category= category)
    for product in products:
        product.isAvailable = False
        product.save()
    category.delete()
    messages.error(request, "Category is deleted")
    return redirect('category_list')

# ====================================================ORDERS================================================================
# Order lIst view
class OrderListView(LoginRequiredMixin, ListView):
    login_url =reverse_lazy('adminLogin')
    model = Order
    template_name = 'orderList.html'
    context_object_name = 'orders'
    paginate_by = 10

# Order search functionality
def OrderSearch(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        orders = Order.objects.order_by('createdDate').filter(Q(user__icontains = keyword) | 
                                                            Q(firstName__icontains = keyword)  | 
                                                            Q(orderNumber__icontains = keyword) | 
                                                            Q(lastName__icontains = keyword)  | 
                                                            Q(email__icontains = keyword)  | 
                                                            Q(phone__icontains = keyword) | 
                                                            Q(addressLineOne__icontains = keyword))
    return render(request, 'orderList.html', {'orders':orders})

# Edit Orders
class OrderUpdateView(LoginRequiredMixin, UpdateView):
    login_url =reverse_lazy('adminLogin')
    template_name = 'editOrder.html'
    model = Order
    fields = ['status']
    success_url = reverse_lazy('order_list')

# View Order
class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url =reverse_lazy('adminLogin')
    context_object_name = 'order'
    model = Order
    template_name = 'orderDetail.html'

def deleteOrder(request, pk):
    order = Order.objects.get(id = pk)
    order.delete()
    order.save()
    return redirect('order_list')


# ============================================DASHBOARD CHART========================================


def sales_chart(request):
    # Get the sales data for the last 7 days
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    sales_data = OrderProduct.objects.filter(created_at__range=(start_date, end_date)).annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('product_price'))

    # Pass the data to the template
    context = {
        'sales_data': sales_data
    }
    return render(request, 'dashboard.html', context)
