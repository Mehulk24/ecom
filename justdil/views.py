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
from decimal import Decimal
from django.db.models import Q


def index(request):
   
    products = Product.objects.filter(
     Q(visible_when_out_of_stock=False)
    ).order_by('-id')

    just_in_products = Product.objects.filter(
         Q(visible_when_out_of_stock=False),
        tags__name__iexact='just_in'
    ).order_by('-id').distinct()

    new_arrivals = Product.objects.filter(
         Q(visible_when_out_of_stock=False),
        tags__name__iexact='Loved_by_You'
    ).order_by('-id').distinct()

    
    banners = HomeBanner.objects.all()
    best_products = BestProduct.objects.all()
    context = {
        'products': just_in_products,
        'new_arrivals': new_arrivals,
        'banners': banners,
        'best_products': best_products,
    }
    return render(request, 'index.html', context)


def hand_collection(request):
    return render(request, 'hand_collection.html')

# def product(request, category=None):
    

   
#     if category == 'All':
#         products = Product.objects.all() 
#     elif category == 'Ring':
#         products = Product.objects.filter(category='Ring')
#     elif category == 'Necklace':
#         products = Product.objects.filter(category='Necklace')
#     elif category == 'Bracelet':
#         products = Product.objects.filter(category='Bracelet')
#     elif category == 'Earring':
#         products = Product.objects.filter(category='Earring')
#     elif category == 'Jewellery_Sets':
#         products = Product.objects.filter(category='Jewellery-Sets')
#     elif category == 'Hair_Accessories':
#         products = Product.objects.filter(category='Hair-Accessories')
#     elif category == 'Toys':
#         products = Product.objects.filter(category='Toys')
#     elif category == 'Bags&More':
#         products = Product.objects.filter(category='Bags&More')
#     elif category == 'E3':
#         products = Product.objects.filter(j_type='e3')
#     elif category == 'Tribe':
#         products = Product.objects.filter(j_type='tribe')
#     else:
#         products = Product.objects.filter(gender_category=category)
#     return render(request, 'product_page.html', {'products': products})
def product(request, category=None):
    category_heading = category or "Collection"

    category_descriptions = {
        'Earring': "From statement trendy earrings to classic Hoops & huggies and charming Studs—your dream ear stack starts here.",
        'Necklace': "Adorn your neckline with elegant pendants, chokers, and layered necklaces.",
        'Ring': "Find stunning rings for every occasion—from delicate bands to bold statement pieces.",
        'Bracelet': "Wrap your wrist in style with charming bangles, cuffs, and chains.",
        'Jewellery_Sets': "Complete your look with our beautifully curated jewelry sets.",
        'Hair_Accessories': "Style your hair with flair—clips, bands, and accessories for all moods.",
        'Toys': "Fun-filled and playful picks for your little ones or inner child.",
        'Bags&More': "Carry your essentials with style—bags, clutches, and more.",
        'E3': "Explore our exclusive E3 jewelry selection—limited and luxurious.",
        'Tribe': "Bold and beautiful tribal designs rooted in heritage and artistry.",
        'Essentials': "Your must-have everyday jewelry—timeless, minimal, and versatile.",
    }

    stock_filter = Q(visible_when_out_of_stock=False)

    if category == 'All':
        products = Product.objects.filter(stock_filter).order_by('-id')

    elif category in ['Ring', 'Necklace', 'Bracelet', 'Earring']:
        products = Product.objects.filter(stock_filter, category=category).order_by('-id')

    elif category == 'Jewellery_Sets':
        products = Product.objects.filter(stock_filter, category='Jewellery-Sets').order_by('-id')

    elif category == 'Hair_Accessories':
        products = Product.objects.filter(stock_filter, category='Hair-Accessories').order_by('-id')

    elif category == 'Toys':
        products = Product.objects.filter(stock_filter, category='Toys').order_by('-id')

    elif category == 'Bags&More':
        products = Product.objects.filter(stock_filter, category='Bags&More').order_by('-id')

    elif category == 'Saturday_Story_Sale':
        products = Product.objects.filter(stock_filter, tags__name__iexact='Saturday_Story_Sale').order_by('-id')

    elif category == 'Loved_by_You':
        products = Product.objects.filter(stock_filter, tags__name__iexact='Loved_by_You').order_by('-id')

    elif category == 'E3':
        products = Product.objects.filter(stock_filter, j_type='e3').order_by('-id')

    elif category == 'Tribe':
        products = Product.objects.filter(stock_filter, j_type='tribe').order_by('-id')

    elif category == 'Essentials':
        products = Product.objects.filter(stock_filter, j_type='Essentials').order_by('-id')

    else:
        products = Product.objects.filter(stock_filter, gender_category=category).order_by('-id')

    return render(request, 'product_page.html', {
        'products': products,
        'category_heading': category_heading,
        'category_description': category_descriptions.get(category, "Explore our beautiful and trendy collections."),
    })



def select(request):
    return render(request, 'w_choise.html')
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
    
PROMO_CODES = {
    'BLINGWELCOME10': 10,  # 10% discount
}


def e_404(request):
    return render(request, '404.html')
    

def favorite_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'favorites.html', {'favorites': favorites})

def add_to_favorites(request, model_name, object_id):
    if not request.user.is_authenticated:
        return redirect('login')

    content_type = ContentType.objects.get(model=model_name)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    )

    if created:
        messages.success(request, "Product added to your wishlist.")
    else:
        messages.info(request, "This product is already in your wishlist.")

    return redirect('favorite_list')

def remove_from_favorites(request, model_name, object_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        content_type = ContentType.objects.get(model=model_name)
        Favorite.objects.filter(user=request.user, content_type=content_type, object_id=object_id).delete()
        return redirect('favorite_list')
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
                    subject="✨ Your One-Time Passcode from Just Lil Bling",
                    message=(
                        f"Dear Customer,\n\n"
                        f"Thank you for choosing us!\n\n"
                        f"Your secure One-Time Passcode (OTP) is: {otp}\n\n"
                        f"Please enter this code on the verification page to continue.\n"
                        f"This OTP is valid for 10 minutes.\n\n"
                        f"— The Just Lil Bling Team\n"
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


def add_to_cart(request, model_type, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    # Choose the model based on type
    if model_type == 'product':
        model = Product
    elif model_type == 'newproduct':
        model = NewProduct
    elif model_type == 'bestproduct':
        model = BestProduct
    else:
        return HttpResponse("Invalid product type", status=400)

    product = get_object_or_404(model, id=product_id)
    content_type = ContentType.objects.get_for_model(model)

    # Get size from POST or fallback
    selected_size = request.POST.get('size') or product.size or ''

    # Get or create cart item
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=product.id,
        total=product.get_discounted_price(),  
        defaults={'size': selected_size}
    )

    # If already in cart, increase quantity and update size if needed
    if not created:
        cart_item.quantity += 1
        cart_item.size = selected_size  # Optionally update size
        cart_item.save()

    return redirect('cart_view')

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        order_id = request.POST.get('cart')

        print(coupon_code)
        print(order_id)

        if not coupon_code or not order_id:
            messages.error(request, 'Missing coupon or order information.')
            return redirect('checkout')  # Replace with your checkout page name


        
        # Check if this is the user's first order (excluding current one)
        has_previous_orders = Order.objects.filter(user=request.user)

        if has_previous_orders:
            messages.error(request, 'This coupon is only valid on your first order.')
            return redirect('checkout')

        # Validate coupon
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
            return redirect('checkout')

        # Apply discount
        if request.session.get('discount_amount'):
            messages.error(request, 'Coupon already applied.')
            return redirect('checkout')
        else:
            discount_percent = coupon.discount_percentage 
            dicount = 0
            discount = (float(order_id) * float(discount_percent))/100 # e.g. 10
            discount_amount = discount
            print(discount_amount)
            request.session['discount_amount'] = discount_amount

        # Update order total
        messages.success(request, f'Coupon applied! You saved ₹{discount_amount:.2f}.')
        return redirect('checkout')

    # If not POST
    return redirect('checkout')


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


    if 'discount_amount' in request.session:
        discount_amount = request.session['discount_amount']
        total_price =float(total_price) - discount_amount
        
        print(total_price) # Clear the discount after applying
    else:
        discount_amount = 0
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
        print(total_price)
        # Create Razorpay order
        razorpay_amount = int(total_price * 100)
        del request.session['discount_amount'] 
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
            'discount_price': discount_amount,
            'total_price': total_price,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order.order_number
        })

    # GET request
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'discount_price': discount_amount,
        'total_price': total_price,
        'razorpay_order_id': '',
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': ''
    })


def remove_c(request):
    if 'discount_amount' in request.session:
        del request.session['discount_amount']
        messages.success(request, "Discount removed successfully.")
    else:
        messages.error(request, "No discount to remove.")

    return redirect('checkout')

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
                coupon_code = "BLINGWELCOME10"
                subject = "Welcome to Just Lil Bling – Enjoy 10% Off!"

                message = (
                    f"Dear {email},\n\n"
                    f"Welcome to Just Lil Bling! We’re thrilled to have you with us.\n\n"
                    f"As a part of our inner circle, you’ll receive early access to exclusive collections, "
                    f"private offers, and curated updates.\n\n"
                    f"To begin your journey, enjoy 10% off your first order with this exclusive code:\n"
                    f"{coupon_code}\n\n"
                    f"Apply it at checkout and experience what we proudly call:\n"
                    f"Affordable Luxury That Won’t Break Your Bank.\n\n"
                    f"Because we believe everyone deserves a little sparkle — without compromise.\n\n"
                    f"With warmest regards\n"
                    f"Hetal Bhatt\n"
                    f"www.justlilbling.com\n"
                    f"care@justlilbling.com"
                )

                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    messages.success(request, "Thanks for subscribing! Check your email for a 10% off coupon.")
                except Exception as e:
                    messages.error(request, f"Subscription saved, but email failed to send: {str(e)}")
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
    

def shipping_returns(request):
    return render(request,"shipping_returns.html")

def founder(request):
    return render(request,"founder.html")




#admin code 

    

# def add_product(request):
    
#     if not request.user.is_staff:
#         return redirect('j_d_admin')
#     else:
#         if request.method == 'POST':
#             product_name = request.POST.get('product_name')
#             product_description = request.POST.get('product_description')
#             product_price = request.POST.get('product_price')
#             product_image = request.FILES.get('product_image')

#             new_product = product(
#                 name=product_name,
#                 description=product_description,
#                 price=product_price,
#                 image=product_image
#             )
#             new_product.save()
#             messages.success(request, "Product added successfully.")
#             return redirect('admin_panel')

#         return render(request, 'admin/admin.html')


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
            size = request.POST.get('size', '')
            price = request.POST['price']
            stock = request.POST['stock']
            description = request.POST.get('description', '')
            image = request.FILES.get('image')
            j_type = request.POST.get('type', '') 
            discount = request.POST.get('p_discount') 



            product = Product.objects.create(
                name=name,
                gender_category=gender_category,
                category=category,
                size=size,
                price=price,
                stock=stock,
                description=description,
                image=image,
                j_type=j_type,
                discount=discount
            )
            for i in range(1, 11):
                color_name = request.POST.get(f'color_name_{i}')
                if color_name :
                    ProductColor.objects.create(
                        product=product,
                        color_name=color_name,
                    )

            selected_categories = request.POST.getlist('product_category')
            for cat_name in selected_categories:
                tag, _ = CategoryTag.objects.get_or_create(name=cat_name)
                product.tags.add(tag)

            # Save multiple gallery images
            gallery_images = request.FILES.getlist('gallery_images')
            for img in gallery_images:
                ProductImage.objects.create(product=product, image=img)

            return redirect('products')  # or your success redirect
        return render(request, "admin/add_product.html")


from .models import Product, NewProduct, BestProduct, ProductImage, ProductColor

def edit_product(request, model_type, product_id):
    if not request.user.is_staff:
        return redirect('j_d_admin')

    # Determine model class
    model_map = {
        'product': Product,
        'newproduct': NewProduct,
        'bestproduct': BestProduct,
    }
    model = model_map.get(model_type)
    if not model:
        return HttpResponse("Invalid product type", status=400)

    product = get_object_or_404(model, id=product_id)

    if request.method == "POST":
        # Basic fields
        product.name = request.POST.get('name', '').strip()
        product.price = request.POST.get('price', '').strip()
        product.stock = request.POST.get('stock', '').strip()
        product.gender_category = request.POST.get('gender_category', '').strip()
        product.category = request.POST.get('category', '').strip()
        product.description = request.POST.get('description', '').strip()
        product.j_type = request.POST.get('type', '').strip()

        # Handle discount (convert safely)
        # try:
        product.discount = request.POST.get('p_discount', 0)
        # except ValueError:
        #     product.discount = 0

        # Handle main image upload
        if 'image' in request.FILES:
            product.image = request.FILES['image']

      

        # Save product first to ensure FK integrity
        product.save()

        # --- Handle Color Fields ---
        ProductColor.objects.filter(product=product).delete()  # Clear existing
        for key in request.POST:
            if key.startswith('color_name_'):
                color_value = request.POST.get(key).strip()
                if color_value:
                    ProductColor.objects.create(product=product, color_name=color_value)

        # --- Handle Gallery Image Deletion ---
        delete_ids = request.POST.getlist('delete_gallery_images')
        if delete_ids:
            ProductImage.objects.filter(id__in=delete_ids, product=product).delete()

        # --- Handle New Gallery Image Uploads ---
        for image_file in request.FILES.getlist('gallery_images'):
            ProductImage.objects.create(product=product, image=image_file)

        # --- Optional: Handle Product Categories (if many-to-many or multiselect) ---
        tag_ids = request.POST.getlist('tags')
        product.tags.set(tag_ids)

        return redirect('products')
    all_tags = CategoryTag.objects.all()
    selected_tags = product.tags.all()

    return render(request, "admin/edit_product.html", {'product': product, 'all_tags': all_tags, 'model_type': model_type,'selected_tags': selected_tags,})


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
            j_type = request.POST.get('type', '') 
            discount = request.POST.get('p_discount') 

            product = NewProduct.objects.create(
                name=name,
                gender_category=gender_category,
                category=category,
                color=color,
                size=size,
                price=price,
                stock=stock,
                description=description,
                image=image,
                j_type=j_type,
                discount=discount
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
        product.name = request.POST.get('name', '').strip()
        product.price = request.POST.get('price', '').strip()
        product.stock = request.POST.get('stock', '').strip()
        # product.j_type = request.POST.get('j_type', '').strip()
        product.color = request.POST.get('color', '').strip()
        product.gender_category = request.POST.get('gender_category', '').strip()
        product.category = request.POST.get('category', '').strip()
        product.description = request.POST.get('description', '').strip()
        product.j_type = request.POST.get('type', '').strip()
        
        
        # Discount field (added)
        product.discount = request.POST.get('p_discount')
        # if discount is not None:
        #     try:
        #         product.discount = int(discount)
        #     except ValueError:
        #         product.discount = 0

        # Handle image if uploaded
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
            j_type = request.POST.get('type', '') 
            discount = request.POST.get('p_discount') 

            product = BestProduct.objects.create(
                name=name,
                gender_category=gender_category,
                category=category,
                color=color,
                size=size,
                price=price,
                stock=stock,
                description=description,
                image=image,
                j_type=j_type,
                discount=discount
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
        product.name = request.POST.get('name', '').strip()
        product.price = request.POST.get('price', '').strip()
        product.stock = request.POST.get('stock', '').strip()
        # product.j_type = request.POST.get('j_type', '').strip()
        product.color = request.POST.get('color', '').strip()
        product.gender_category = request.POST.get('gender_category', '').strip()
        product.category = request.POST.get('category', '').strip()
        product.description = request.POST.get('description', '').strip()
        product.j_type = request.POST.get('type', '').strip()
        
        
        # Discount field (added)
        product.discount = request.POST.get('p_discount')
        # if discount is not None:
        #     try:
        #         product.discount = int(discount)
        #     except ValueError:
        #         product.discount = 0

        # Handle image if uploaded
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
    
    
def toggle_visibility(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Only staff allowed
    if not request.user.is_staff:
        return redirect('j_d_admin')

    product.visible_when_out_of_stock = 'visible' in request.POST
    product.save()

    return redirect(request.POST.get('redirect_to', 'products')) 
