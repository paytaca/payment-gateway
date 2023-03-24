from django.contrib import admin
from PaymentGateway.models import WoocommerceOrder
# Register your models here.

class WoocommerceOrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer_name", "status", "created_at", "updated_at", "total")
    list_filter = ("created_at", "status")
    search_fields = ("order_id", "customer_name", "status")

    def has_add_permission(self, request, obj=None):
        return False
    

admin.site.register(WoocommerceOrder, WoocommerceOrderAdmin)