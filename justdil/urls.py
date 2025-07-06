from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('product/<str:category>/',views.product,name='product'),
    path('product_detail/<int:p_id>',views.p_detail,name='p_detail'),
    path('new_arrival/<int:n_id>',views.new_arrival,name='new_arrival'),
    path('best_selling_product/<int:b_id>',views.best_product_page,name='best_product_page'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<str:model_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<str:model_type>/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('login/',views.user_login,name='login'),
    path('register/',views.signup,name='register'),
    path('about/',views.about,name='about'),
    path('faq/',views.faq,name='faq'),
    path('profile/', views.user_profile, name='user_profile'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('subscribe_email/', views.subscribe_email, name='subscribe_email'),
    path('verify_otp/', views.otp, name='verify_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('shipping_returns/', views.shipping_returns, name='shipping_returns'),
    path('founder/', views.founder, name='founder'),
    path('remove_coupon/', views.remove_c, name='remove_c'),
    path('404/', views.e_404, name='e_404'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/add/<str:model_name>/<int:object_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<str:model_name>/<int:object_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('select/',views.select, name='select'),
    path('Hampers/', views.hand_collection, name='hampers'),


    #Admin
    path('logout/',views.user_logout,name='logout'),
    path('just_deal_admin_page/',views.admin_login,name='j_d_admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('orders/', views.orders, name='orders'),
    path('products/', views.products, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<str:model_type>/<int:product_id>/', views.edit_product, name='edit_product'),

    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('new-arrivals/add/', views.add_new_arrival, name='add_new_arrival'),
    path('banners/manage/', views.manage_banners, name='manage_banners'),
    path('remove-banner/<int:banner_id>/', views.remove_banner, name='remove_banner'),
    path('add_new_arrival/', views.add_new_aravie, name='add_new_aravie'),
    path('delete_new_arrival/<int:new_arrival_id>/', views.delete_new_arrival, name='delete_new_arrival'),
    path('edit_new_arrival/<int:new_arrival_id>/', views.edit_new_arrival, name='edit_new_arrival'),
    path('best_product/',views.best_product,name='best_product'),
    path('add_best_product/', views.add_best_product, name='add_best_product'),
    path('delete_best_product/<int:new_arrival_id>/', views.delete_best_product, name='delete_best_product'),
    path('edit_best_product/<int:new_arrival_id>/', views.edit_best_product, name='edit_best_product'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('orders/<int:order_id>/view/', views.view_order, name='view_order'),
    path('products/toggle/<int:product_id>/', views.toggle_visibility, name='toggle_visibility'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)