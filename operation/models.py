from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.

class Client(models.Model):
    client_id = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    client_lastname = models.CharField(max_length=100)
    client_address = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=100)
    client_email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.client_id} | {self.client_name} {self.client_lastname}"

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Factura #{self.invoice_id}"

class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Warehouse: {self.name}"

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
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, null=True)
    section = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.barcode} | {self.name}"
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    status = models.CharField(max_length=100, default="En proceso")
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, null=True, unique=True)

    def __str__(self):
        return f"Orden #{self.order_id}"
    
class Claim(models.Model):
    TIPO_RECLAMO_CHOICES = [
        ('mala atención', 'Mala atención'),
        ('local en mal estado', 'Local en mal estado'),
        ('otro', 'Otro'),
    ]
    claim_id = models.AutoField(primary_key=True)
    Orden = models.ForeignKey('Order', on_delete=models.CASCADE)
    Tipo_de_reclamo = models.CharField(max_length=100, choices=TIPO_RECLAMO_CHOICES, default='Otro')
    Descripcion_de_reclamo = models.CharField(max_length=1000)
    Nombre = models.CharField(max_length=100)
    Correo = models.EmailField(max_length=100, default="su_correo@gmail.com")
    Fecha = models.DateField(default=timezone.now, editable=False)

    def __str__(self):
        return f"Reclamo #{self.claim_id} | {self.Tipo_de_reclamo} | {self.Estado_de_reclamo}"