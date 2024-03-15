from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
import uuid
from django.db import IntegrityError
# Create your views here.


def index(request):
    products=Product.objects.all()
    item_name=request.GET.get('item_name')
    sort=request.GET.get('sort_by')
    # search code
    if item_name!='' and item_name is not None:
        products=Product.objects.filter(title__icontains=item_name) | Product.objects.filter(category__icontains=item_name)
    if sort=='price_low_to_high':
        products=products.order_by('price')
    elif sort=='price_high_to_low':
        products=products.order_by('-price')
    elif sort=='new':
        products=products.order_by('-date')
    elif sort=='old':
        products=products.order_by('date')
    # paginator code
    paginator=Paginator(products,2)
    page_number=request.GET.get('page')
    products=paginator.get_page(page_number)
    wishlist_count = 0
    cart_count = 0
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist_count = wishlist.product.count() if wishlist else 0
        cart = Cart.objects.filter(user=request.user).first()
        cart_count = cart.product.count() if cart else 0
    return render(request,'index.html',{'products':products,'wishlist_count':wishlist_count,'cart_count':cart_count})


def detail(request,id):
    product=get_object_or_404(Product, id=id)
    wishlist_count = 0
    cart_count = 0
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist_count = wishlist.product.count() if wishlist else 0
        cart = Cart.objects.filter(user=request.user).first()
        cart_count = cart.product.count() if cart else 0
    return render(request, 'detail.html', {'product':product,'wishlist_count':wishlist_count,'cart_count':cart_count})


def wishlist(request):
    if request.method == 'POST':
        wishlist_data = request.POST.get('wishlist_data')
        if  wishlist_data :
            wishlist_data=json.loads(wishlist_data)
            ids=list(wishlist_data.keys())
            wishlist=[]
            for id in ids:
                product=Product.objects.get(id=int(id))
                wishlist.append(product)
            return render(request, 'wishlist.html', {'wishlist': wishlist}) 
    else:
        return redirect('shop:index')
    return render(request, 'wishlist.html')


def wishlist_login(request):
    wishlist,created=Wishlist.objects.get_or_create(user=request.user)
    wishlist_count = wishlist.product.count() if wishlist else 0
    cart=Cart.objects.filter(user=request.user).first()
    cart_count=cart.product.count() if cart else 0
    if request.method == 'POST':                  
        product_id = int(request.POST.get('product_id'))
        product=Product.objects.get(id=product_id)
        if product in wishlist.product.all():
            messages.info(request, 'Product already in wishlist')
            return redirect('shop:wishlist_login')
        wishlist.product.add(product)
        return redirect('shop:index')
    else:
        available_products = wishlist.product.all() 
        return render(request, 'wishlist_login.html', {'available_products': available_products,'wishlist_count':wishlist_count,'cart_count':cart_count})
    

def remove_wishlist(request, id):
    wishlist = Wishlist.objects.filter(user=request.user).first()
    wishlist.product.remove(id)
    return redirect('shop:wishlist_login')



@login_required(login_url='users:user_login')
def cart(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user).first()
    wishlist_count = wishlist.product.count() if wishlist else 0
    cart_count=cart.product.count() if cart else 0
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        print(product_id)
        product=Product.objects.get(id=product_id)
        cart.product.add(product)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('shop:index')
    available_products=cart.product.all() if cart else []
    ava_pro = [(item.product, item.quantity) for item in cart.cartitem_set.all()] if cart else []

    sum=0
    disc=0
    for p,q in ava_pro:
        sum=sum+(p.price * q)
        disc=disc+(p.discount_price *q)
    return render(request, 'cart.html', {'cart_count':cart_count,'wishlist_count':wishlist_count,'ava_pro':ava_pro,'sum':sum,'disc':disc})

def remove_cart(request,id):
    cart=Cart.objects.filter(user=request.user).first()
    cart.product.remove(id)
    return redirect('shop:cart')

def add_product_cart(request,id):
    product=Product.objects.get(id=id)
    cart=Cart.objects.filter(user=request.user).first()
    cartitem=CartItem.objects.filter(cart=cart, product=product).first()

    cartitem.quantity += 1
    cartitem.save()
    return redirect('shop:cart')


def remove_product_cart(request, id):
    product=Product.objects.get(id=id)
    cart=Cart.objects.filter(user=request.user).first()
    cartitem=CartItem.objects.filter(cart=cart, product=product).first()
    if cartitem:
        cartitem.quantity -= 1
        if cartitem.quantity <= 0:
            cartitem.delete()
        else:
            cartitem.save()
    return redirect('shop:cart')


@login_required(login_url='users:user_login')
@require_POST
def checkout(request):
    if request.method=='POST':
        price = float(request.POST.get('price')) 
        quantity=1.0
        if request.POST.get('quant'):
            quantity=float(request.POST.get('quant'))
        price=price*quantity
        address=Address.objects.filter(user=request.user).first()
        print(address)
        return render(request, 'checkout.html',{
            'price':price,
            'address':address
        })


def user_address(request):
    if request.method == 'POST':
        address = request.POST.get('loc')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        address_obj, created = Address.objects.get_or_create(user=request.user)
        address_obj.address = address
        address_obj.city = city
        address_obj.state = state
        address_obj.zipcode = zipcode
        address_obj.save()
        return render(request,'proceed.html')
    


def add_product(request):
    if request.method == 'POST':
        user=request.user
        title = request.POST.get('title')
        category = request.POST.get('category')
        price = request.POST.get('price')
        discount_price = request.POST.get('dis-price')
        description = request.POST.get('description')
        image=request.POST.get('image')
        product = Product.objects.create(user=user,title=title, category=category, price=price, discount_price=discount_price, description=description,image=image)
        return redirect('shop:index')
    return render(request, 'add_product.html')

def view_product(request):
    products=Product.objects.filter(user=request.user)
    item_name=request.GET.get('item_name')
    sort=request.GET.get('sort_by')
    if item_name!='' and item_name is not None:
        products=products.objects.filter(title__icontains=item_name) | products.objects.filter(category__icontains=item_name)
    paginator=Paginator(products,2)
    page_number=request.GET.get('page')
    products=paginator.get_page(page_number)
    return render(request, 'view_product.html', {'products':products})

def update_product(request, id):
    product=Product.objects.get(user=request.user,id=id)
    if request.method == 'POST':
        product.title=request.POST.get('title')
        product.category=request.POST.get('category')
        product.price=request.POST.get('price')
        product.discount_price=request.POST.get('dis-price')
        product.description=request.POST.get('description')
        product.image=request.POST.get('image')
        product.save()
        return redirect('shop:view_product')
    return render(request, 'update_product.html', {'product':product})

def delete_product(request, id):
    product=Product.objects.get(user=request.user, id=id)
    product.delete()
    return redirect('shop:view_product')


