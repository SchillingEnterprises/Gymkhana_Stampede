from django.contrib import admin

from .models import Customer, Employee, Inventory, StoreBranch, Transaction

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Inventory)
admin.site.register(StoreBranch)
admin.site.register(Transaction)
