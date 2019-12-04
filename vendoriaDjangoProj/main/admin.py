from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('User Types', {'fields': ('is_customer', 'is_marketer', 'is_shipper', 'is_manufacturer',
                                   'is_inventory_worker', 'is_manager')}),
    )


admin.site.register(User, CustomUserAdmin)

models_to_register = (
    Customer,
    Shipper,
    Region,
    Manufacturer,
    Product,
    Place,
    Purchase,
    Inventory,
    Cart,
    Contract,
    Saved_Card,
    Ships_To,
    Shipment,
    Reorder,
    Makes,
)

for m in models_to_register:
    admin.site.register(m)
