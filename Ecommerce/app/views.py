# from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, Product, Customer
from django.db.models import Count, Q
from .forms import CustomerRegistrationForm, CustomerProfileForm,MyPasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# from django import HttpResponse
# Create your views here.
 
def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title').annotate(total=Count("title"))
        return render(request, 'app/category.html', locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())

class CustomerRegistrationView(View):
    def  get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals() ) 
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! You have registered successfully.")
        else:
            messages.warning(request, "Invalid input. Please try again.")
        return render(request, "app/customerregistration.html", locals())


class ProfileView(LoginRequiredMixin, View):
    login_url = '/accounts'
    redirect_field_name = 'next'
    
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())        
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            
            reg.save()
            messages.success(request, "Profile Saved Successfully!")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/profile.html", locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    form = CustomerProfileForm()
    return render(request, 'app/address.html', locals())

class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST, instance=add)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Address Updated Successfully!")
            return redirect('address')
        messages.warning(request, "Please correct the errors below.")
        return render(request, 'app/updateAddress.html', locals())
    
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            messages.success(request, f"{product.title} added to cart successfully!")
            
            if request.POST.get('buy_now'):
                return redirect('show_cart')
            return redirect('product-detail', pk=product_id)
    return redirect('home')

@login_required
def show_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.total_cost for item in cart_items)
    return render(request, 'app/addtocart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@login_required
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                return redirect('show_cart')
        elif action == 'remove':
            cart_item.delete()
            return redirect('show_cart')
        
        cart_item.save()
        return redirect('show_cart')
    return redirect('show_cart')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        try:
            prod_id = request.GET.get('prod_id')
            if not prod_id:
                return JsonResponse({'error': 'Product ID is required'}, status=400)
            
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            cart_item.quantity += 1
            cart_item.save()
            
            cart_items = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            totalamount = amount + 40  # Delivery charge
            
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        try:
            prod_id = request.GET.get('prod_id')
            if not prod_id:
                return JsonResponse({'error': 'Product ID is required'}, status=400)
            
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            cart_item.quantity = max(1, cart_item.quantity - 1)  # Ensure quantity doesn't go below 1
            cart_item.save()
            
            cart_items = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            totalamount = amount + 40  # Delivery charge
            
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        try:
            prod_id = request.GET.get('prod_id')
            if not prod_id:
                return JsonResponse({'error': 'Product ID is required'}, status=400)
            
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            cart_item.delete()
            
            cart_items = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            totalamount = amount + 40  # Delivery charge
            
            data = {
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    
    if not cart_items:
        return redirect('show_cart')
        
    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    totalamount = amount + 40  # 40 is delivery charge
    
    context = {
        'add': add,
        'cart_items': cart_items,
        'totalamount': totalamount,
        'amount': amount
    }
    return render(request, 'app/checkout.html', context)

@login_required
def payment(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    totalamount = amount + 40  # Delivery charge

    if request.method == 'POST':
        # Here you would integrate with a payment gateway
        # For now, simulate payment success and clear the cart
        items = list(cart_items)
        cart_items.delete()
        messages.success(request, 'Payment successful! Your order has been placed.')
        # Store receipt data in session for /receipt/
        request.session['last_amount'] = amount
        request.session['last_totalamount'] = totalamount
        request.session['last_items'] = [
            {'product': {'title': item.product.title, 'discounted_price': item.product.discounted_price}, 'quantity': item.quantity}
            for item in items
        ]
        request.session['last_date'] = timezone.now().strftime('%d %B %Y, %I:%M %p')
        return redirect('receipt')

    return render(request, 'app/payment.html', {'amount': amount, 'totalamount': totalamount})

@login_required
def receipt(request):
    user = request.user
    # For demo: show the most recent paid order (simulate with last payment)
    # In a real app, you would fetch the last order from an Order model
    # Here, just show an empty receipt or a message if no recent payment
    amount = request.session.get('last_amount')
    totalamount = request.session.get('last_totalamount')
    items = request.session.get('last_items')
    date = request.session.get('last_date')
    if not all([amount, totalamount, items, date]):
        return render(request, 'app/receipt.html', {
            'amount': 0,
            'totalamount': 0,
            'items': [],
            'user': user,
            'date': timezone.now().strftime('%d %B %Y, %I:%M %p'),
            'error': 'No recent order found.'
        })
    return render(request, 'app/receipt.html', {
        'amount': amount,
        'totalamount': totalamount,
        'items': items,
        'user': user,
        'date': date
    })