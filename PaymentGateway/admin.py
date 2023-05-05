from django.contrib import admin
from PaymentGateway.models import Order, User, Storefront, Product, OrderItem, TotalSales, TotalSalesYesterday, TotalSalesByMonth, TotalSalesByYear
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ("store", "order_id", "customer_name", "status", "created_at", "updated_at", "total", "total_bch", "payment_method", "total_received")
    list_filter = ("store", "created_at", "status")
    search_fields = ("order_id", "customer_name", "status")

    def has_add_permission(self, request, obj=None):
        return False
    
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "full_name", "email", "username", "password", "xpub_key", "wallet_hash", "created_at")
    list_filter = ("user_id", "created_at")
    search_fields = ("username",)

class StorefrontAdmin(admin.ModelAdmin):
    list_display = ("user", "store_type", "store_url", "key", "secret", "created_at", "updated_at")
    list_filter = ("user", "store_type", "created_at", "updated_at")
    search_fields = ("user",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("store", "product_id", "name", "price")
    list_filter = ("store", "name")
    search_fields = ("store",)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "order", "store", "quantity", "price")
    list_filter = ("product", "order", "store")
    search_fields = ("product", "order", "store")

class TotalSalesAdmin(admin.ModelAdmin):
    list_display = ("store", "total_sale", "total_orders", "products_sold", "total_customers", "date_created", "total_sale_percentage", "total_orders_percentage", "products_sold_percentage", "total_customers_percentage")
    list_filter = ("store", "total_sale")

    def has_add_permission(self, request, obj=None):
        return False

class TotalSalesYesterdayAdmin(admin.ModelAdmin):
    list_display = ("store", "total_sale", "total_orders", "products_sold", "total_customers", "date_created")
    list_filter = ("store", "total_sale")

    def has_add_permission(self, request, obj=None):
        return False
        
class TotalSalesByMonthAdmin(admin.ModelAdmin):
    list_display = ("store", "month", "total_sale")
    list_filter = ("store", "month", "total_sale")

    def has_add_permission(self, request, obj=None):
        return False
    
class TotalSalesByYearAdmin(admin.ModelAdmin):
    list_display = ("store", "year", "total_sale")
    list_filter = ("store", "year", "total_sale")

    def has_add_permission(self, request, obj=None):
        return False
    
admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Storefront, StorefrontAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(TotalSales, TotalSalesAdmin)
admin.site.register(TotalSalesYesterday, TotalSalesYesterdayAdmin)
admin.site.register(TotalSalesByMonth, TotalSalesByMonthAdmin)
admin.site.register(TotalSalesByYear, TotalSalesByYearAdmin)