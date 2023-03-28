from django.contrib import admin
from PaymentGateway.models import WoocommerceOrder, User, KeyAndSecret
# Register your models here.

class WoocommerceOrderAdmin(admin.ModelAdmin):
    list_display = ("username", "order_id", "customer_name", "status", "created_at", "updated_at", "total")
    list_filter = ("username", "created_at", "status")
    search_fields = ("order_id", "customer_name", "status")

    def has_add_permission(self, request, obj=None):
        return False
    
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "password", "created_at")
    list_filter = ("user_id", "created_at")
    search_fields = ("username",)

class KeyAndSecretAdmin(admin.ModelAdmin):
    list_display = ("username", "consumer_key", "consumer_secret", "created_at", "updated_at")
    list_filter = ("username", "created_at", "updated_at")
    search_fields = ("username",)

admin.site.register(WoocommerceOrder, WoocommerceOrderAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(KeyAndSecret, KeyAndSecretAdmin)