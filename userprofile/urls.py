from django.contrib.auth import views as auth_views
from django.urls import path
from userprofile import views
from django.shortcuts import redirect

app_name='userprofile'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'),name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path("myaccount/", views.myaccount, name="myaccount"),
    path('mystore/',views.my_store,name='mystore'),
    path('mystore-order-detail/',views.my_order_detail,name='my_order_detail'),
    path('mystore-order-detail/<int:pk>/',views.my_store_order_detail,name='my_store_order_detail'),
    path('mystore/addproduct/',views.add_product,name='addproduct'),
    path('mystore/edit-product/<int:pk>/',views.edit_product,name='editproduct'),
    path('mystore/delete-product/<int:pk>/',views.delete_product,name='deleteproduct'),
    path('vendors/<int:pk>/',views.verdor_detail,name='vendor_detail'),
    
]
