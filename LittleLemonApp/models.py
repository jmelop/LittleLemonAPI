from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=35)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name