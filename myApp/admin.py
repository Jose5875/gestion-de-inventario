from django.contrib import admin
from .models import Product,Sales_Details,Sale,Supplier,Category,Customer,Employee,Inventory

# Register your models here.
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Sales_Details)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Inventory)