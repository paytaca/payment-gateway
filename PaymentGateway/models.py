from django.db import models

# Create your models here.

class WoocommerceOrder(models.Model):
    order_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    