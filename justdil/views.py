from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Max
from django.core.mail import send_mail
import random
from django.conf import settings
import razorpay

def index(request):
    print(request.user)
    products = Product.objects.all()
    new_arrivals = NewProduct.objects.all()
    banners = HomeBanner.objects.all()
    best_products = BestProduct.objects.all()
    context = {
        'products': products,
        'new_arrivals': new_arrivals,
        'banners': banners,
        'best_products': best_products,
    }
    return render(request, 'index.html', context)

def product(request, category=None):
    if category == 'All':
        new_arrivals = NewProduct.objects.all()
        products = Product.objects.all() 
    elif category == 'Ring':
        products = BestProduct.objects.filter(category='Ring')
    elif category == 'Necklace':
        products = Product.objects.filter(category='Necklace')
    elif category == 'Bracelet':
        products = Product.objects.filter(category='Bracelet')
    elif category == 'Earring':
        products = Product.objects.filter(category='Earring')
    else:
        products = Product.objects.filter(gender_category=category)
    return render(request, 'product_page.html', {'products': products})

def p_detail(request,p_id):
    product = get_object_or_404(Product, id=p_id)
    context = {
        'product': product,
        'available_sizes': ['S', 'M', 'L', 'XL'],  # Or make dynamic based on stock
        'available_colors': [
            ('#FFD700', 'Gold'),
            ('#000000', 'Black'),
            ('#C0C0C0', 'Silver')
        ]
    }

    return render(request, 'p_details.html',context)

def new_arrival(request,n_id):
    new_product = get_object_or_404(NewProduct, id=n_id)
    return render(request, 'new_arrival.html', {'product': new_product})

def best_product_page(request,b_id):
    best_product = get_object_or_404(BestProduct, id=b_id)
    return render(request, 'best_product_page.html', {'product': best_product})
    



def cart(request):
    return render(request, 'cart.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Authenticate user

        if user is not None:
            login(request, user) 
            
            request.session['user_id'] = user.id  
            request.session['username'] = user.username

            return redirect('index')  
        else:
            messages.error(request, "Invalid username or password")  # Show error message

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')

        if password == c_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                # Generate a 6-digit OTP
                otp = str(random.randint(100000, 999999))
                
                # Store user data & OTP temporarily in session
                request.session['signup_data'] = {
                    'username': username,
                    'email': email,
                    'password': password,
                    'otp': otp
                }

                # Send OTP email
                send_mail(
                    subject="✨ Your One-Time Passcode from Just Lib Bling",
                    message=(
                        f"Dear Customer,\n\n"
                        f"Thank you for choosing us!\n\n"
                        f"Your secure One-Time Passcode (OTP) is: {otp}\n\n"
                        f"Please enter this code on the verification page to continue.\n"
                        f"This OTP is valid for 10 minutes.\n\n"
                        f"Stay golden,\n"
                        f"— The Just Lib Bling Team\n"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.info(request, "An OTP has been sent to your email. Please verify.")
                return redirect('verify_otp')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'signup.html')

def otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        signup_data = request.session.get('signup_data')
        print(signup_data)
        print(entered_otp)

        if signup_data and entered_otp == signup_data.get('otp'):
            user = User.objects.create_user(
                username=signup_data['username'],
                email=signup_data['email'],
                password=signup_data['password']
            )
            login(request, user)
            del request.session['signup_data']  # Clean up
            messages.success(request, "Account created and verified successfully!")
            return redirect('index')  # or another page
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')


def user_logout(request):
    request.session.flush()
    return redirect('index')

from django.db import IntegrityError


def add_to_cart(request, product_id, model_type):
    if not request.user.is_authenticated:
        return redirect('login')
    
    else:

        if model_type == 'product':
            model = Product
        elif model_type == 'newproduct':
            model = NewProduct
        elif model_type == 'bestproduct':
            model = BestProduct
        else:
            return HttpResponse("Invalid product type", status=400)

        content_type = ContentType.objects.get_for_model(model)
        product = get_object_or_404(model, id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=product.id
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart_view')


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)

        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def update_cart(request, cart_id, model_type):
    if model_type == "product":
        model = Product
    elif model_type == "newproduct":
        model = NewProduct
    else:
        return HttpResponse("Invalid product type")

    content_type = ContentType.objects.get_for_model(model)
    
    cart_item = get_object_or_404(Cart, user=request.user, content_type=content_type, object_id=cart_id)

    if request.method == "POST":
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            cart_item.quantity = max(1, cart_item.quantity - 1)
        else:
            cart_item.quantity = quantity

        cart_item.save()

    return redirect('cart_view')
@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return HttpResponse("Your cart is empty.", status=400)

    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        order_number = generate_unique_order_number()
        while Order.objects.filter(order_number=order_number).exists():
            order_number = generate_unique_order_number()

        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            zip_code=request.POST.get('zip'),
            phone=request.POST.get('phone'),
            total=total_price,
            order_status='Pending',
            order_number=order_number
        )

        for item in cart_items:
            content_type = ContentType.objects.get_for_model(item.product.__class__)
            OrderItem.objects.create(
                order=order,
                content_type=content_type,
                object_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price
            )

        # Create Razorpay order
        razorpay_amount = int(total_price * 100)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            "amount": razorpay_amount,
            "currency": "INR",
            "payment_capture": 1,
            "notes": {
                "order_id": order.order_number
            }
        })

        order.razorpay_order_id = razorpay_order['id']
        order.save()

        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order.order_number
        })

    # GET request
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': '',
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': ''
    })

def generate_unique_order_number():
    last_order = Order.objects.aggregate(max_id=Max('id'))['max_id']
    next_id = (last_order or 0) + 1
    return f"JD{next_id:04d}"

def order_success(request):
    payment_id = request.GET.get('payment_id')

    if not payment_id:
        return HttpResponse("Missing payment_id", status=400)

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        # Fetch payment details
        payment = client.payment.fetch(payment_id)
        print("Razorpay Payment Response:", payment)

        # Get order_number stored in Razorpay notes
        order_number = payment.get('notes', {}).get('order_id')
        if not order_number:
            return HttpResponse("Order ID not found in Razorpay payment notes", status=400)

        # Find your order from DB
        order = get_object_or_404(Order, order_number=order_number)
        order.pyment_status = 'Paid'
        order.save()
        cart_items = Cart.objects.filter(user=request.user)
        cart_items.delete()

        # Send confirmation email
        send_mail(
            subject="Order Confirmation",
            message=(
                f"Dear {order.first_name},\n\n"
                f"Thank you for your order!\n"
                f"Your order number is: {order.order_number}\n"
                f"Total Amount: ₹{order.total}\n\n"
                f"Stay golden,\n"
                f"— The Just Lib Bling Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )
        messages.success(request, "Order placed successfully!")
        # Render success page
        

        return render(request, 'order_success.html', {
            'payment': payment,
            'order': order
        })

    except Exception as e:
        return HttpResponse(f"Error verifying payment: {e}", status=500)

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')


def user_dashboard(request):
    return render(request, 'dashboard.html')

def user_profile(request):
    return render(request, 'profile.html')

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')  # after saving redirect to profile page

    return render(request, 'edit_profile.html')



def user_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__content_type')

    for order in orders:
        # Dynamically access the product for each order item
        for item in order.items.all():
            item.product_obj = item.content_type.get_object_for_this_type(id=item.object_id)
        order.items_list = order.items.all()

    return render(request, 'user_orders.html', {'orders': orders})

def subscribe_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                coupon_code = "JDL10OFF"

                try:
                    send_mail(
                        subject="Thanks for Subscribing – Enjoy 10% Off!",
                        message=(
                            f"Hi there!\n\n"
                            f"Thank you for subscribing to our jewelry updates.\n\n"
                            f"Here’s your exclusive 10% OFF coupon code: {coupon_code}\n"
                            f"Use it at checkout to sparkle for less!\n\n"
                            f"Stay golden,\n"
                            f"— The Just Lib Bling Team"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.error(request, f"Subscription saved, but email failed: {str(e)}")

                messages.success(request, "Thanks for subscribing! Check your email for a 10% off coupon.")
            else:
                messages.info(request, "You're already subscribed.")
    return redirect('/')


def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp_code')  # Or fetch from DB
        
        if user_otp == session_otp:
            messages.success(request, "OTP verified successfully!")
            return redirect('dashboard')  # or any destination
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.session.get('otp_email')  # Store user email in session during signup

        if not user_email:
            messages.error(request, "No email found. Please sign up again.")
            return redirect('register')

        # Generate a new 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Save the new OTP in session
        request.session['otp'] = otp

        # Send the OTP via email
        try:
            send_mail(
                subject="✨ Your One-Time Passcode from Just Lib Bling",
                message=(
                    f"Dear Customer,\n\n"
                    f"Thank you for choosing us!\n\n"
                    f"Your secure One-Time Passcode (OTP) is: {otp}\n\n"
                    f"Please enter this code on the verification page to continue.\n"
                    f"This OTP is valid for 10 minutes.\n\n"
                    f"Stay golden,\n"
                    f"— The Just Lib Bling Team\n"
                    f"www.yourjewelrysite.com"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            messages.success(request, "A new OTP has been sent to your email.")
        except Exception as e:
            messages.error(request, f"Failed to send OTP: {str(e)}")

        return redirect('verify_otp')



#admin code 

    

def add_product(request):
    
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            product_description = request.POST.get('product_description')
            product_price = request.POST.get('product_price')
            product_image = request.FILES.get('product_image')

            new_product = product(
                name=product_name,
                description=product_description,
                price=product_price,
                image=product_image
            )
            new_product.save()
            messages.success(request, "Product added successfully.")
            return redirect('admin_panel')

        return render(request, 'admin/admin.html')


def dashboard(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        total_products = Product.objects.count()
        total_sales = Order.objects.aggregate(total=Sum('total'))['total'] or 0
        total_stock = Product.objects.aggregate(total=Sum('stock'))['total'] or 0
        recent_products = Product.objects.order_by('-id')[:5]  # Show last 5 added products



        context = {
            'total_products': total_products,
            'total_sales': total_sales,
            'total_stock': total_stock,
            'recent_products': recent_products
        }
        
        return render(request, "admin/dashboard.html", context)

def users(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        user = User.objects.all()
        return render(request, "admin/users.html", {'users': user})

def orders(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        query = request.GET.get('q', '')
        if query:
            orders_data = Order.objects.filter(customer__icontains=query)
        else:
            orders_data = Order.objects.all()

        return render(request, "admin/orders.html", {'orders': orders_data})
    
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('users')


def products(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        query = request.GET.get('q', '')  # Get the search query from the request
        if query:
            product_list = Product.objects.filter(name__icontains=query)  # Filter products based on search query
        else:
            product_list = Product.objects.all()  # Show all products if no query is given

        return render(request, "admin/products.html", {'products': product_list, 'query': query})

def add_product(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        if request.method == 'POST':
            name = request.POST['name']
            gender_category = request.POST['gender_category']
            category = request.POST['category']
            color = request.POST['color']
            size = request.POST.get('size', '')
            price = request.POST['price']
            stock = request.POST['stock']
            description = request.POST.get('description', '')
            image = request.FILES.get('image')

            product = Product.objects.create(
                name=name,
                gender_category=gender_category,
                category=category,
                color=color,
                size=size,
                price=price,
                stock=stock,
                description=description,
                image=image
            )

            # Save multiple gallery images
            gallery_images = request.FILES.getlist('gallery_images')
            for img in gallery_images:
                ProductImage.objects.create(product=product, image=img)

            return redirect('products')  # or your success redirect
        return render(request, "admin/add_product.html")


def edit_product(request, product_id):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        product = get_object_or_404(Product, id=product_id)
        print(product.image)

        if request.method == "POST":
            product.name = request.POST['name']
            product.price = request.POST['price']
            product.stock = request.POST['stock']
            product.size = request.POST.get('size', '')
            
            # Ensure color is retrieved correctly
            color_value = request.POST.get('color', '').strip()
            if color_value:
                product.color = color_value

            product.gender_category = request.POST.get('gender_category', '') 
            product.category = request.POST.get('category', '')  
            product.description = request.POST.get('description', '')  

            if 'image' in request.FILES:
                product.image = request.FILES['image']

            product.save()
            return redirect('products')

        return render(request, "admin/edit_product.html", {'product': product})


def delete_product(request, product_id):

    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('products')


def add_new_arrival(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        query = request.GET.get('q', '')  # Get the search query from the request
        if query:
            product_list = NewProduct.objects.filter(name__icontains=query)  # Filter products based on search query
        else:
            product_list = NewProduct.objects.all()  # Show all products if no query is given

        return render(request, "admin/new_arrival_form.html", {'products': product_list, 'query': query})

def add_new_aravie(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:

        if request.method == 'POST':
            name = request.POST['name']
            gender_category = request.POST['gender_category']
            category = request.POST['category']
            color = request.POST['color']
            size = request.POST.get('size', '')
            price = request.POST['price']
            stock = request.POST['stock']
            description = request.POST.get('description', '')
            image = request.FILES.get('image')

            product = NewProduct.objects.create(
                name=name,
                gender_category=gender_category,
                category=category,
                color=color,
                size=size,
                price=price,
                stock=stock,
                description=description,
                image=image
            )

            # Save multiple gallery images
            gallery_images = request.FILES.getlist('gallery_images')
            for img in gallery_images:
                NewProductImage.objects.create(product=product, image=img)

            return redirect('add_new_arrival')  # or your success redirect
        return render(request, "admin/add_new_Arive.html")

def delete_new_arrival(request, new_arrival_id):
    new_arrival = NewProduct.objects.get(id=new_arrival_id)
    new_arrival.delete()
    return redirect('add_new_arrival')


def edit_new_arrival(request, new_arrival_id):
    product = get_object_or_404(NewProduct, id=new_arrival_id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.size = request.POST.get('size', '')
        
        # Ensure color is retrieved correctly
        color_value = request.POST.get('color', '').strip()
        if color_value:
            product.color = color_value

        product.gender_category = request.POST.get('gender_category', '') 
        product.category = request.POST.get('category', '')  
        product.description = request.POST.get('description', '')  

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('add_new_arrival')

    return render(request, "admin/edit_new_product.html", {'product': product})


def best_product(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:
        query = request.GET.get('q', '') 
        if query:
            product_list = BestProduct.objects.filter(name__icontains=query) 
        else:
            product_list = BestProduct.objects.all()  

        return render(request, "admin/best_product.html", {'products': product_list, 'query': query})

def add_best_product(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:

        if request.method == 'POST':
            name = request.POST['name']
            gender_category = request.POST['gender_category']
            category = request.POST['category']
            color = request.POST['color']
            size = request.POST.get('size', '')
            price = request.POST['price']
            stock = request.POST['stock']
            description = request.POST.get('description', '')
            image = request.FILES.get('image')

            product = BestProduct.objects.create(
                name=name,
                gender_category=gender_category,
                category=category,
                color=color,
                size=size,
                price=price,
                stock=stock,
                description=description,
                image=image
            )

            # Save multiple gallery images
            gallery_images = request.FILES.getlist('gallery_images')
            for img in gallery_images:
                BestProductImage.objects.create(product=product, image=img)

            return redirect('best_product')  # or your success redirect
        return render(request, "admin/add_best_product.html")

def delete_best_product(request, new_arrival_id):
    new_arrival = BestProduct.objects.get(id=new_arrival_id)
    new_arrival.delete()
    return redirect('add_best_product')


def edit_best_product(request, best_product_id):
    product = get_object_or_404(BestProduct, id=best_product_id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.size = request.POST.get('size', '')
        
        # Ensure color is retrieved correctly
        color_value = request.POST.get('color', '').strip()
        if color_value:
            product.color = color_value

        product.gender_category = request.POST.get('gender_category', '') 
        product.category = request.POST.get('category', '')  
        product.description = request.POST.get('description', '')  

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('add_best_product')

    return render(request, "admin/edit_best_product.html", {'product': product})


def manage_banners(request):
    if not request.user.is_staff:
        return redirect('j_d_admin')
    else:

        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            images = request.FILES.getlist('images')

            for image in images[:3]:  # Limit to 3 images
                HomeBanner.objects.create(title=title, description=description, image=image)

            return redirect('manage_banners')

        banners = HomeBanner.objects.all()  
        return render(request, 'admin/manage_banners.html', {'banners': banners})


def remove_banner(request, banner_id):
    if request.method == 'POST':
        # Get the banner by ID and delete it
        banner = get_object_or_404(HomeBanner, id=banner_id)
        banner.delete()

    # Redirect back to the banners page or admin panel
    return redirect('manage_banners')


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.first_name = request.POST['first_name']
        order.last_name = request.POST['last_name']
        order.email = request.POST['email']
        order.address = request.POST['address']
        order.city = request.POST['city']
        order.zip_code = request.POST['zip_code']
        order.phone = request.POST['phone']
        order.order_status = request.POST['order_status']
        order.save()
        return redirect('orders')

    return render(request, 'admin/edit_order.html', {'order': order})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('orders')


def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate and log the user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the admin dashboard
    else:
        form = AuthenticationForm()

    return render(request, 'admin/admin_login.html', {'form': form})


def view_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = order.items.all()  # assuming related name is `items`
    return render(request, 'admin/view_order.html', {'order': order, 'order_items': order_items})
