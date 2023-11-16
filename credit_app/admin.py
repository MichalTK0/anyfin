from django.contrib import admin
from .models import Customer, Policy, CustomerPolicy

# Register your models here.
admin.site.register(Customer)
admin.site.register(Policy)
admin.site.register(CustomerPolicy)
