from unicodedata import category
from django.shortcuts import render

from registration.models import Profile
from .models import Contact
from .forms import ContactForm
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from django.core.paginator import Paginator
from .models import MyCart
from django.contrib import messages

# Create your views here.


# Create your views here.
def home(request):
    newarrivalprod = Product.objects.all().order_by('-id')[:4]
    newtrendingprod = Product.objects.filter(trending="Yes").order_by("id")[:4]
    newpopularprod = Product.objects.filter(popular="Yes").order_by("id")[:4]
    if request.user.is_authenticated:
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        cartprodcount = ''
    context = {
        'newarrivalprod': newarrivalprod,
        'newtrendingprod': newtrendingprod,
        'newpopularprod': newpopularprod,
        'cartprodcount': cartprodcount,
    }
    return render(request, 'home/index.html', context)

def products(request):
    allprod = Product.objects.all().order_by('?')
    paginator = Paginator(allprod, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    total_pages = page_obj.paginator.num_pages
    pages = []
    pp = int(page_number) - 2
    p = int(page_number) - 1
    pn = int(page_number)
    n = int(page_number) + 1
    nn = int(page_number) + 2
    set1 = {pp, p, pn, n, nn}
    for i in range(total_pages):
        i+=1
        pages.append(i)
    set2 = set(pages)
    set3 = set1.intersection(set2)
    pagelist = list(set3)
    if request.user.is_authenticated:
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        cartprodcount = ''
    context = {
        'allprod':page_obj,
        'pagelist':pagelist,
        'currentpage':pn,
        'cartprodcount': cartprodcount,
    }
    return render(request, 'home/products.html', context)

def productdetail(request, id):
    product = Product.objects.get(id=id)
    relatedprod = Product.objects.all().order_by('?')[:4]
    favoritemessage = ''
    if request.user.is_authenticated:
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
        productexists = MyCart.objects.filter(user=request.user, product=product)
        cartprodtotal = 0
        for cart in cartprod:
            quanprice = cart.quantity * cart.product.selling_price
            cartprodtotal += quanprice
        if productexists.exists():
            productincart = 'Yes'
        else:
            productincart = 'No'
        print(productincart)
    else:
        cartprod = []
        cartprodcount = ''
        productincart = ''
        cartprodtotal = 0
    context = {
        'product':product,
        'relatedprod':relatedprod,
        'favoritemessage':favoritemessage,
        'cartprodcount': cartprodcount,
        'productincart': productincart,
        'cartprod': cartprod,
        'cartprodtotal': cartprodtotal,
    }
    return render(request, 'home/productdetail.html', context)

def cart(request):
    otherprod = Product.objects.all().order_by('?')[:4]
    if request.user.is_authenticated:
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        cartprodcount = ''
        cartprod = ''
    context = {
        'otherprod': otherprod,
        'cartprod': cartprod,
        'cartprodcount': cartprodcount,
        }
    return render(request, 'home/cart.html', context)

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        id = request.POST.get('prod_id')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=id)
        user = request.user
        print(id, product, quantity, user.username)
        mycart, created = MyCart.objects.get_or_create(user=user, product=product)
        if created:
            mycart.quantity = int(quantity)
            print('I am just created')
        else:
            mycart.quantity += 1
            print('I am added')
        mycart.save()
        proqty = mycart.quantity
        print(mycart.quantity)
        selling_price = product.selling_price
        sub_total = proqty * product.selling_price
        print(sub_total)
        cartproduct = [c for c in MyCart.objects.filter(user=request.user)]
        cartproducts = {}
        print(cartproduct)
        for i in range(len(cartproduct)):
            if cartproduct[i].id not in cartproducts.keys():
                cartproducts[cartproduct[i].id] = {
                    'cart_id': cartproduct[i].id,
                    'sub_total': cartproduct[i].sub_total,
                    'user_id':cartproduct[i].user.id,
                    'prod_id':cartproduct[i].product.id,
                    'prod_name': cartproduct[i].product.name,
                    'prod_price': cartproduct[i].product.selling_price,
                    'prod_quantity': cartproduct[i].quantity,
                    'prod_image_url': cartproduct[i].product.photo.url,
                    }
        cartproductcount = MyCart.objects.filter(user=request.user).count()
        print(cartproductcount)
        data = {'proqty':proqty, 'action':'add', 'selling_price':selling_price, 'sub_total': sub_total, 'cartproducts':cartproducts, 'cartproductcount':cartproductcount}
        return JsonResponse(data)

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        id = request.POST.get('prod_id')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=id)
        user = request.user
        print(id, product, quantity, user.username)
        mycart = MyCart.objects.get(user=user, product=product)
        mycart.quantity -= int(quantity)
        print('I am subtracted')
        mycart.save()
        proqty = mycart.quantity
        if mycart.quantity == 0:
            mycart.delete()
        product.save()
        print(mycart.quantity)
        selling_price = product.selling_price
        sub_total = proqty * product.selling_price
        product_id = product.id
        print(sub_total)
        cartproduct = [c for c in MyCart.objects.filter(user=request.user)]
        cartproducts = {}
        print(cartproduct)
        for i in range(len(cartproduct)):
            if cartproduct[i].id not in cartproducts.keys():
                cartproducts[cartproduct[i].id] = {
                    'cart_id': cartproduct[i].id,
                    'user_id':cartproduct[i].user.id,
                    'sub_total': cartproduct[i].sub_total,
                    'prod_id':cartproduct[i].product.id,
                    'prod_name': cartproduct[i].product.name,
                    'prod_price': cartproduct[i].product.selling_price,
                    'prod_quantity': cartproduct[i].quantity,
                    'prod_image_url': cartproduct[i].product.photo.url,
                    }
        cartproductcount = MyCart.objects.filter(user=request.user).count()
        print(cartproductcount)
        data = {'product_id':product_id, 'proqty':proqty, 'action':'subt', 'selling_price':selling_price, 'sub_total': sub_total, 'cartproducts':cartproducts, 'cartproductcount':cartproductcount}
        return JsonResponse(data)

@csrf_exempt
def delete_from_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id','')
        product = Product.objects.get(id=prod_id)
        product_cart = MyCart.objects.get(user=request.user, product=product)
        rowId = product_cart.product.id
        prod_sub_total = product_cart.sub_total
        print(prod_sub_total)
        product_cart.delete()
        cartproductcount = MyCart.objects.filter(user=request.user).count()
        data = {'rowId': rowId, 'prod_sub_total': prod_sub_total, 'cartproductcount': cartproductcount}
        return JsonResponse(data)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('full_name')
            subject = form.cleaned_data.get('subject')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            message = form.cleaned_data.get('message')
            contact = Contact(full_name=name, email=email, subject=subject, phone=phone, message=message)
            contact.save()
            messages.success(request, 'Your message has been sent successfully!!')
            return redirect('home')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'home/contact.html', context)

def about(request):
    return render(request, 'home/about.html')
