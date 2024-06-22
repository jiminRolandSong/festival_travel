from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Festival)
admin.site.register(Package)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
