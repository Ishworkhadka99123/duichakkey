from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import AutoField
from registration.models import Customer
from math import floor
# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

TRENDING_CHOICES = (('Yes', 'Yes'),('No','No'),)
POPULAR_CHOICES = (('Yes', 'Yes'),('No','No'),)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trending = models.CharField(choices=TRENDING_CHOICES, max_length=10, default='No')
    popular = models.CharField(choices=POPULAR_CHOICES, max_length=10, default="No")
    marked_price = models.FloatField()
    selling_price = models.FloatField()
    available_quantity = models.PositiveIntegerField(default=0) #Remove this default option in the final project
    photo = models.ImageField(upload_to='products/')
    #Char Field For image alt #####-------Needed to be added--------#####
    return_policy = models.CharField(max_length=255)
    tags = models.CharField(max_length=300, default='')
    modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        discount = (self.marked_price - self.selling_price)/self.marked_price
        return str(floor(discount * 100))

    def delete(self, using=None, keep_parents=False):
        self.photo.storage.delete(self.photo.name)
        super().delete()

class MyCart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def sub_total(self):
        return str(self.quantity * self.product.selling_price)

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.subject + '...' + '    By   ' + self.full_name)