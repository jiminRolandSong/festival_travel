from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import Category, Festival, Package, Order, OrderItem, Cart
from .serializers import *
from django.contrib.auth.models import User, Group
from datetime import date

OrderItem.objects.all().delete()

# Create your views here.
def home(request):
    path = request.path
    return render(request, "home.html")

def categories(request):
    categories = Category.objects.all()
    cate_dict = {'cate': categories}
    return render(request, 'categories.html', cate_dict)

class CategoriesAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
def festivals(request):
    festivals = Festival.objects.all()
    fest_dict = {"fest": festivals}
    return render(request, 'festivals.html', fest_dict)
 
class FestivalsAPIView(generics.ListCreateAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    ordering_fields = ['start_date']
    filterset_fields = ['start_date']
    search_fields = ['title']
    
    def get_permissions(self):
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]
    
def show_festival(request, slug=None):
    if slug:
        festival = Festival.objects.get(slug=slug)
        packages = Package.objects.filter(festival=festival)
    else:
        festival = ""
    return render(request, 'festival_item.html', {"festival": festival, 'packages': packages})
        
    
class SingleFestivalAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]
    
def packages(request):
    packages = Package.objects.all()
    pack_dict = {"packages": packages}
    return render(request, 'packages.html', pack_dict)
    
class PackagesAPIView(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    ordering_fields = ['price']
    filterset_fields = ['price', 'festival', 'category']
    search_fields = ['title']
    
    def get_permissions(self):
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]
    
def show_package(request, slug=None):
    if slug:
        package = Package.objects.get(slug=slug)
    else:
        package = ""
    return render(request, 'package_item.html', {"package": package})
    
class SinglePackageAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]
    
def add_to_cart(request, slug):
    package = get_object_or_404(Package, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user, package=package, quantity=1, price=package.price)
    
    if not created:
        cart.quantity += 1
    cart.save()
    
    return redirect('cart')

def cart(request):
    cart = Cart.objects.filter(user=request.user)
    cart_dict = {'cart': cart}
    return render(request, "cart.html", cart_dict)
    
class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def delete(self, request):
        user = request.user
        Cart.objects.filter(user=user).delete()    
        return Response()
    
def checkout(request):
    user = request.user
    cartItems = Cart.objects.filter(user = user)
    if not cartItems:
        redirect('cart')
    total_price = 0
    total_quantity = 0
    order = Order.objects.create(user = user,
                            total_quantity = total_quantity,
                            total_price = total_price,
                            status = False,
                            date = date.today())
    for cart in cartItems:
        OrderItem.objects.create(user = user,
                                 order = order,
                                     package = cart.package,
                                     quantity = cart.quantity,
                                     price = cart.price)
        order.total_price += cart.price
        order.total_quantity += 1

    order.save()
    cartItems.delete()
    return redirect('current-order', id = order.id)

def current_order(request, id):
    order = Order.objects.get(id=id)
    order_dict = {'order': order}
    return render(request, 'current_order.html', order_dict)
    
class OrderAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def get(self, request):
        user = request.user
        if request.user.groups.filter(name='managers').exists():
            queryset = OrderItem.objects.all()
            serializer = OrderItemSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = OrderItem.objects.filter(user = user)
            serializer = OrderItemSerializer(queryset, many=True)
            return Response(serializer.data)
        
    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cartItems = Cart.objects.filter(user = user)
        total_price = 0
        total_quantity = 0
        order = Order.objects.create(user = user,
                                total_quantity = total_quantity,
                                total_price = total_price,
                                status = False,
                                date = date.today())
        for cart in cartItems:
            OrderItem.objects.create(user = user,
                                    order = order,
                                        package = cart.package,
                                        quantity = cart.quantity,
                                        price = cart.price)
        order.total_price += cart.price
        order.total_quantity += 1
        cartItems.delete()
        return Response()
    
class OrderItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def get(self, request, pk):
        queryset = Order.objects.filter(user = pk)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
        
    def delete(self, request, pk):
        if request.user.groups.filter(name='managers').exists():
            Order.objects.filter(user = pk).delete()
            return Response()
        return Response()     
        