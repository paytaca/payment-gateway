from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Account(models.Model):
    user_id = models.AutoField(primary_key=True, null=False, unique=True)
    full_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    username = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    xpub_key = models.CharField(max_length=255, null=True)
    wallet_hash = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='accounts')
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.pk:
            auth_user = User.objects.create_superuser(
                username=self.email,
                email=self.email,
                password=self.password
            )
            self.password = make_password(self.password)
            self.auth_user = auth_user
        super(Account, self).save(*args, **kwargs)
        
    @staticmethod
    def get_account_from_token(token):
        try:
            token = Token.objects.get(key=token)
            user = token.user
            if user:
                return user
            else:
                return None
        except Token.DoesNotExist:
            return None
    
    # def save(self, *args, **kwargs):
    #     self.password = make_password(self.password)
    #     super(User, self).save(*args, **kwargs) 

class Storefront(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    store_type = models.CharField(max_length=255, null=False,)
    store_url = models.CharField(max_length=255, null=False, unique=True)
    key = models.CharField(max_length=255, null=False)
    secret = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_url
    
class Order(models.Model):
    store = models.ForeignKey(Storefront, to_field="store_url", on_delete=models.CASCADE)
    order_id = models.IntegerField()
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_bch = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    payment_method = models.CharField(max_length=255, default="")
    total_received = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    def __str__(self):
        return str(self.order_id)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    store = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, default=0, decimal_places=2)
    
class TotalSales(models.Model):
    store = models.ForeignKey(Storefront, to_field="store_url", on_delete=models.CASCADE)
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.IntegerField(default=0)
    products_sold = models.IntegerField(default=0)
    total_customers = models.IntegerField(default=0)
    total_sale_percentage = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    total_orders_percentage = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    products_sold_percentage = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    total_customers_percentage = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    date_created = models.DateField(blank=True, null=True)

class TotalSalesYesterday(models.Model):
    store = models.ForeignKey(Storefront, to_field="store_url", on_delete=models.CASCADE)
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.IntegerField(default=0)
    products_sold = models.IntegerField(default=0)
    total_customers = models.IntegerField(default=0)
    date_created = models.DateField(blank=True, null=True)
    
class TotalSalesByMonth(models.Model):
    store = models.ForeignKey(Storefront, to_field="store_url", on_delete=models.CASCADE)
    month = models.CharField(max_length=7) # YYYY-MM format
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)

class TotalSalesByYear(models.Model):
    store = models.ForeignKey(Storefront, to_field="store_url", on_delete=models.CASCADE)
    year = models.IntegerField()
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)







