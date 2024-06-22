from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Category, Festival, Package, Order, OrderItem, Cart
from .serializers import *
from django.contrib.auth.models import User, Group

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
    else:
        festival = "hi"
    return render(request, 'festival_item.html', {"festival": festival})
        
    
class SingleFestivalAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    
    def get_permissions(self):
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]
    
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
    
class SinglePackageAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    
    def get_permissions(self):
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]
    
class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def delete(self, request):
        user = request.user
        Cart.objects.filter(user=user).delete()    
        return Response()
    
class OrderItemAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def get(self, request):
        user = request.user
        if request.user.groups.filter(name='Manager').exists():
            queryset = OrderItem.objects.all()
            serializer = OrderItemSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = OrderItem.objects.filter(order = user)
            serializer = OrderItemSerializer(queryset, many=True)
            return Response(serializer.data)
        
    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cartItems = Cart.objects.filter(user = user)
        total_price = 0
        total_quantity = 0
        for cart in cartItems:
            OrderItem.objects.create(user = user,
                                     package = cart.package,
                                     quantity = cart.quantity,
                                     price = cart.price)
            total_price += cart.price
            total_quantity += 1
        Order.objects.create(user = user,
                            total_quantity = total_quantity,
                            total_price = total_price,
                            status = True,
                            date = '2024-05-23')
        cartItems.delete()
        return Response()
    
class OrderAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def get(self, request, pk):
        queryset = Order.objects.filter(user = pk)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
        
    def delete(self, request, pk):
        if request.user.groups.filter(name='Manager').exists():
            Order.objects.filter(user = pk).delete()
            return Response()
        return Response()     
        