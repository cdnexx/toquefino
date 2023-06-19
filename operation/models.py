from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.order} | {self.product} | {self.quantity}"

class Product(models.Model):
    barcode_validator = RegexValidator(r'^[0-9]{10}$', 'Barcode must be a 10-digit number')
    barcode = models.CharField(max_length=10, unique=True, validators=[barcode_validator])
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    stock_min = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.barcode} | {self.name}"
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    status = models.CharField(max_length=100, default="En proceso")

    def __str__(self):
        return f"Orden #{self.order_id}"