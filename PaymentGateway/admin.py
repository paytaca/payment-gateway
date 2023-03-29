from django.contrib import admin
from PaymentGateway.models import Order, User, Storefront
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "store", "order_id", "customer_name", "status", "created_at", "updated_at", "total")
    list_filter = ("user", "store", "created_at", "status")
    search_fields = ("user", "order_id", "customer_name", "status")

    def has_add_permission(self, request, obj=None):
        return False
    
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "password", "created_at")
    list_filter = ("user_id", "created_at")
    search_fields = ("username",)

class StorefrontAdmin(admin.ModelAdmin):
    list_display = ("user", "store_type", "store_url", "key", "secret", "created_at", "updated_at")
    list_filter = ("user", "store_type", "created_at", "updated_at")
    search_fields = ("user",)

admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Storefront, StorefrontAdmin)