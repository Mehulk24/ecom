from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(N_Users)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(NewProduct)
admin.site.register(Coupon)
admin.site.register(ProductColor)
admin.site.register(CategoryTag)