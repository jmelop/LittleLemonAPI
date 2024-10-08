from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    name = models.CharField(max_length=35)
    unit_price = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.menuitem.name}"

class Order(models.Model):
    STATUS_CHOICES = [(0, 'Out for delivery'), (1, 'Delivered')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, related_name='delivery_orders', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.menuitem.name}"