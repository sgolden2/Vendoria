from django.contrib import admin
from .models import *
# Register your models here.

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