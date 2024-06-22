from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    def __str__(self) -> str:
        return self.title
    
class Festival(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.title


class Package(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    featured = models.BooleanField(db_index=True)
    availability = models.BooleanField(db_index=True)
    
    def __str__(self) -> str:
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self) -> str:
        return str(self.id)    
       
      

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(db_index=True, default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.id)

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self) -> str:
        return str(self.id)
