"""vendoriaDjangoProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('header/', views.header, name='header'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('register/customer/', views.CustomerRegistrationView.as_view(), name='customer_registration'),
    path('register/marketer/', views.MarketerRegistrationView.as_view(), name='marketer_registration'),
    path('register/manufacturer/', views.ManufacturerRegistrationView.as_view(), name='manufacturer_registration'),
    path('register/inventory/', views.InventoryRegistrationView.as_view(), name='inventory_registration'),
    path('register/shipper/', views.ShipperRegistrationView.as_view(), name='shipper_registration'),
    path('register/manager/', views.ManagerRegistrationView.as_view(), name='manager_registration'),
    path('logout/', views.logout_page, name='logout'),

    path('products/', views.customer_page, name='customer_page'),
    path('data-center/', views.marketer_page, name='marketer_page'),
    path('manufacturer-center/', views.manufacturer_page, name='manufacturer_page'),
    path('inventory/', views.inventory_page, name='inventory_page'),
    path('shipper-center/', views.shipper_page, name='shipper_page'),
    path('manager-console/', views.manager_page, name='manager_page'),

    path('contracts/', views.contracts, name='contracts'),
    path('cards/', views.cards, name='cards'),
]
