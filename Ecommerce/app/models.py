from django.db import models

# Create your models here.

CATEGORY_CHOICES = (
    ('CR', 'Curd'),
    ('ML', 'Milk'),
    ('LS', 'Lassi'),
    ('MS', 'Milkshake'),
    ('PN', 'Paneer'),
    ('GH', 'Ghee'),
    ('CZ', 'Cheese'),
    ('IC', 'Ice Cream'),
    # Add more categories as needed
)

STATE_CHOICES = (
    ('PB', 'Punjab'),
    ('SD', 'Sindh'),
    ('KP', 'Khyber Pakhtunkhwa'),
    ('BL', 'Balochistan'),
    ('GB', 'Gilgit-Baltistan'),
    ('IS', 'Islamabad Capital Territory'),
    ('AJK', 'Azad Jammu and Kashmir'),
    # Add more provinces/territories as needed
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price  = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField()
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    
    def __str__(self):
        return self.title 
    

from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=108)

    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} - {self.quantity} pcs"
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price    