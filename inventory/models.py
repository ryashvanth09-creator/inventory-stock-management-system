from django.db import models

# Create your models here.
from django.db import models


# Category Table
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Supplier Table
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Customer Table
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Product Table
class Product(models.Model):
    name = models.CharField(max_length=100)

    sku = models.CharField(
        max_length=50,
        unique=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=0)

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reorder_level = models.PositiveIntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Stock In Table
class StockIn(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


# Stock Out Table
class StockOut(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"