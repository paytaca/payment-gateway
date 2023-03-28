from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True, null=False)
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs) 

class WoocommerceOrder(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class KeyAndSecret(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    store_url = models.CharField(max_length=255, null=False)
    consumer_key = models.CharField(max_length=255, null=False)
    consumer_secret = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    