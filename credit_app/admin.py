from django.contrib import admin
from .models import Customer, Policy, CustomerPolicy


class CustomerPolicyAdmin(admin.ModelAdmin):
    # Make the accepted and rejection reason fields read_only on the admin panel.
    readonly_fields = ["accepted", "rejection_reason"]


# Register all models
admin.site.register(Customer)
admin.site.register(Policy)
admin.site.register(CustomerPolicy, CustomerPolicyAdmin)
