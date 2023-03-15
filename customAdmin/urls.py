from django.urls import path,include
from . import views

urlpatterns = [
    path('login/',views.adminLogin, name='admin_login'),
    path('admin_dashboard/', views.dashboard, name='admin_dashboard'),
    path('searchUser/',views.searchUser, name='searchUser'),
    path('createUser/',views.createUser,name='createUser'),
    path('updateUser/<int:id>/',views.updateUser,name='updateUser'),
    path('deleteUser/<int:id>/',views.deleteUser, name='deleteUser'),

    path('test/',views.test, name='test'),
]

