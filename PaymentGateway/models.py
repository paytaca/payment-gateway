from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

''' kanan pagtesting han pasa pasa chuchu '''
# class Test(models.Model):
#     xpub_key = models.CharField(max_length=255, null=False, default="a1")
#     wallet_hash = models.CharField(max_length=255, null=False, default="a2")

class User(models.Model):
    user_id = models.AutoField(primary_key=True, null=False)
    full_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    username = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    xpub_key = models.CharField(max_length=255, null=False, default="a1")
    wallet_hash = models.CharField(max_length=255, null=False, default="a2")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs) 

class Storefront(models.Model):
    user = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
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

class TotalSales(models.Model):
    store = models.ForeignKey(Storefront, to_field="store_url", on_delete=models.CASCADE)
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)
    
class TotalSalesByMonth(models.Model):
    store = models.ForeignKey(Storefront, to_field="store_url", on_delete=models.CASCADE)
    month = models.CharField(max_length=7) # YYYY-MM format
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)

class TotalSalesByYear(models.Model):
    store = models.ForeignKey(Storefront, to_field="store_url", on_delete=models.CASCADE)
    year = models.IntegerField()
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)







