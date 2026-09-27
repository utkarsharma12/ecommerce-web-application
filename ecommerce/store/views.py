from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Order, OrderItem
from .forms import UserRegisterForm, UserLoginForm, CheckoutForm
from .cart import Cart


def home(request):
    """Product listings with optional search and category filters."""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    
    products = Product.objects.all().order_by('-created_at')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
        
    if category:
        products = products.filter(category__iexact=category)
        
    categories = Product.objects.exclude(category='').values_list('category', flat=True).distinct()
    
    return render(
        request,
        'store/home.html',
        {
            'products': products,
            'categories': categories,
            'selected_category': category,
            'query': query,
        }
    )


def product_detail(request, product_id):
    """Detailed view for a single product."""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4] if product.category else Product.objects.exclude(id=product.id)[:4]

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product,
            'related_products': related_products,
        }
    )


def cart_detail(request):
    """Display items in the user's shopping cart."""
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, product_id):
    """Add a product to cart or increment quantity."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = 1
    override = False
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1
        override = request.POST.get('override', 'false').lower() == 'true'
    else:
        try:
            quantity = int(request.GET.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

    if product.stock <= 0:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'This product is out of stock.'}, status=400)
        messages.error(request, f'Sorry, "{product.name}" is currently out of stock.')
        return redirect('home')

    cart.add(product=product, quantity=quantity, override_quantity=override)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': len(cart),
            'total_price': str(cart.get_total_price()),
            'message': f'"{product.name}" added to cart!'
        })

    messages.success(request, f'Added "{product.name}" to your cart.')
    return redirect('cart')


def cart_decrement(request, product_id):
    """Decrease quantity of a product in the cart by 1."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrement(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': len(cart),
            'total_price': str(cart.get_total_price()),
        })
        
    return redirect('cart')


def cart_remove(request, product_id):
    """Remove a product completely from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': len(cart),
            'total_price': str(cart.get_total_price()),
        })

    messages.info(request, f'Removed "{product.name}" from your cart.')
    return redirect('cart')


def cart_clear(request):
    """Clear all products from the cart."""
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Your cart has been cleared.")
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    """Checkout process: collect shipping info and place order."""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add products before checking out.")
        return redirect('home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Check stock availability for all cart items
            for item in cart:
                prod = item['product']
                if item['quantity'] > prod.stock:
                    messages.error(
                        request,
                        f'Insufficient stock for "{prod.name}". Available: {prod.stock}, In Cart: {item["quantity"]}.'
                    )
                    return redirect('cart')

            # Create Order
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.status = 'Processing'
            order.save()

            # Create OrderItems and decrement stock
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
                product = item['product']
                product.stock = max(0, product.stock - item['quantity'])
                product.save()

            # Clear cart
            cart.clear()
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('order_success', order_id=order.id)
    else:
        # Prepopulate with logged in user details if available
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)

    return render(
        request,
        'store/checkout.html',
        {
            'cart': cart,
            'form': form,
            'total_amount': cart.get_total_price(),
        }
    )


@login_required(login_url='login')
def order_success(request, order_id):
    """Confirmation page shown after placing an order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required(login_url='login')
def order_history(request):
    """List of all previous orders for the logged in user."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required(login_url='login')
def order_detail(request, order_id):
    """Detailed view for a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to MyStore, {user.username}! Your account was created successfully.")
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next') or 'home'
                return redirect(next_url)
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')