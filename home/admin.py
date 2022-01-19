from django.contrib import admin
from .models import Category, Product, MyCart, Contact
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'available_quantity', 'selling_price', 'return_policy', 'tags', 'modified_date']

@admin.register(MyCart)
class MyCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'date_created']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['sno', 'full_name', 'email', 'message', 'created_at']