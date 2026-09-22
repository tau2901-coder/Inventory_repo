"""
URL configuration for InventoryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from testapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('add_item/', views.add_item),
    path('view_item/', views.view_item),
    path('edit_item/<int:id>/', views.edit_item, name="edit_item"),
    path('delete_item/<int:id>/', views.delete_item, name="delete_item"),
    #-------------Unit-----------------------------
    path('view_unit/', views.view_unit),
    path('add_unit/', views.add_unit),
    path('edit_unit/<int:id>/', views.edit_unit, name="edit_unit"),
    path('delete_unit/<int:id>/', views.delete_unit, name="delete_unit"),
    #------------------Brand-------------------
    path('brand_view/', views.brand_view),
    path('add_brand/', views.add_brand),
    path('edit_brand/<int:id>/', views.edit_brand, name="edit_brand"),
    path('delete_brand/<int:id>/', views.delete_brand, name="delete_brand"),
#------------------------Auth----------------------------------------
    path('signup_view/', views.signup_view),
    path('user_detail/', views.user_detail),
    path('login_view/', views.login_view),
    path('logout_view/', views.logout_view),
    path('change_password/', views.change_password, name='change_password'),
#--------------------Purchase--------------------------------------
    path('view_purchase_mstr/', views.view_purchase_mstr),
    path('add_purchase_full/', views.add_purchase_full),
    path('edit_purchase_mstr/<int:id>/', views.edit_purchase_mstr, name="edit_purchase_mstr"),
    path('delete_purchase_mstr/<int:id>/', views.delete_purchase_mstr, name="delete_purchase_mstr"),
    path('view_purchase_deatils/', views.view_purchase_details),
    path('edit_purchase_details/<int:id>/', views.edit_purchase_details, name="edit_purchase_details"),
    path('delete_purchase_details/<int:id>/', views.delete_purchase_details, name="delete_purchase_details"),
#---------------------------------Sales-------------------------------------
    path('view_sales_master/', views.view_sales_master),
    path('add_sales_full/', views.add_sales_full),
    path('edit_sales_master/<int:id>/', views.edit_sales_master, name="edit_sales_master"),
    path('delete_sales_master/<int:id>/', views.delete_sales_master, name="delete_sales_master"),
    path('view_sales_details/', views.view_sales_details),
    path('edit_sales_details/<int:id>/', views.edit_sales_details, name="edit_sales_details"),
#------------------------Search Sales and Purchase--------------------------
    path('search_purchase_report/', views.search_purchase_report),
    path('search_sales_report/', views.search_sales_report),
    path('view_purchase_detail_single/<int:id>/', views.view_purchase_detail_single, name="view_purchase_detail_single"),
    path('view_sales_detail_single/<int:id>/', views.view_sales_detail_single,name="view_sales_detail_single"),
]
