from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import Category, Festival, Package, Order, OrderItem, Cart
from .serializers import *
from django.contrib.auth.models import User, Group
from datetime import date

OrderItem.objects.all().delete()

# Homepage of the website
def home(request):
    return render(request, "home.html")

# View to list all categories of Festival Travel Packages
def categories(request):
    categories = Category.objects.all()
    cate_dict = {'cate': categories}
    return render(request, 'categories.html', cate_dict)

# API view for listing and creating categories
class CategoriesAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# View to list all festivals
def festivals(request):
    festivals = Festival.objects.all()
    fest_dict = {"fest": festivals}
    return render(request, 'festivals.html', fest_dict)

# API view for listing and creating festivals, allowing filtering, ordering, and search 
class FestivalsAPIView(generics.ListCreateAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    ordering_fields = ['start_date'] # Allow ordering by start date
    filterset_fields = ['start_date'] # Allow filtering by start date
    search_fields = ['title'] # Allow searching by title
    
    def get_permissions(self):
        # No permission required for GET, but admin privileges required for other methods
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]

# View to display specific festival details and its associated packages  
def show_festival(request, slug=None):
    if slug:
        festival = Festival.objects.get(slug=slug)
        packages = Package.objects.filter(festival=festival)
    else:
        festival = ""
    return render(request, 'festival_item.html', {"festival": festival, 'packages': packages})
        
# API view for retrieving, updating, or deleting a single festival (identified by slug)   
class SingleFestivalAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        # No permission required for GET, but admin privileges required for other methods
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]

# View to list all packages   
def packages(request):
    packages = Package.objects.all()
    pack_dict = {"packages": packages}
    return render(request, 'packages.html', pack_dict)
  
# API view for listing and creating packages, with filtering, ordering, and search    
class PackagesAPIView(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    ordering_fields = ['price']  # Allow ordering by price
    filterset_fields = ['price', 'festival', 'category'] # Allow filtering by price, festival, and category
    search_fields = ['title'] # Allow searching by title
    
    def get_permissions(self):
        # No permission for GET, admin required for other actions
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]

# View to display specific package details    
def show_package(request, slug=None):
    if slug:
        package = Package.objects.get(slug=slug)
    else:
        package = ""
    return render(request, 'package_item.html', {"package": package})

# API view for retrieving, updating, or deleting a single package (identified by slug)    
class SinglePackageAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if(self.request.method == "GET"):
            return []
        
        return [IsAdminUser()]

# View to add a package to the cart, increments quantity if already in cart    
def add_to_cart(request, slug):
    package = get_object_or_404(Package, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user, package=package, quantity=1, price=package.price)
    
    if not created: # If the cart item already exists, increment quantity
        cart.quantity += 1
    cart.save() # Save the cart item
    
    return redirect('cart') # Redirect to the cart page

# View to display all cart items for the user
def cart(request):
    cart = Cart.objects.filter(user=request.user) # Fetch all cart items for the current user
    cart_dict = {'cart': cart}
    return render(request, "cart.html", cart_dict)

# API view to list and create cart items, restricted to authenticated users    
class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def delete(self, request):
        user = request.user
        Cart.objects.filter(user=user).delete()    
        return Response()

# View to handle the checkout process for the current user's cart    
def checkout(request):
    user = request.user
    cartItems = Cart.objects.filter(user = user)
    if not cartItems: # If the cart is empty, redirect to cart
        redirect('cart')
        
    total_price = 0
    total_quantity = 0
    
    # Create a new order with default values
    order = Order.objects.create(user = user,
                            total_quantity = total_quantity,
                            total_price = total_price,
                            status = False,
                            date = date.today())
    
    # Loop through each cart item and create order items
    for cart in cartItems:
        orderitem = OrderItem.objects.create(user = user,
                                 order = order,
                                     package = cart.package,
                                     quantity = cart.quantity,
                                     price = cart.price)
        orderitem.save()
        order.total_price += cart.price
        order.total_quantity += 1

    order.save()
    cartItems.delete()  # Clear the user's cart after checkout
    return redirect('current-order', id = order.id) # Redirect to the current order view

# View to display a completed order by its ID
def current_order(request, id):
    order = Order.objects.get(id=id)
    order_dict = {'order': order}
    return render(request, 'current_order.html', order_dict)

# API view to list and create order items, restricted to authenticated users    
class OrderAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    # GET request for listing orders, managers see all orders, users see only their own
    def get(self, request):
        user = request.user
        if request.user.groups.filter(name='managers').exists():
            queryset = Order.objects.all()
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = Order.objects.filter(user = user)
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data)
    
    # POST request for creating an order from the user's cart    
    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cartItems = Cart.objects.filter(user = user)
        
        total_price = 0
        total_quantity = 0
        
        # Create a new order
        order = Order.objects.create(user = user,
                                total_quantity = total_quantity,
                                total_price = total_price,
                                status = False,
                                date = date.today())
        
        # Loop through cart items and create order items
        for cart in cartItems:
            orderitem = OrderItem.objects.create(user = user,
                                    order = order,
                                        package = cart.package,
                                        quantity = cart.quantity,
                                        price = cart.price)
            orderitem.save()
        order.total_price += cart.price
        order.total_quantity += 1
        cartItems.delete()
        return Response()

# View to check the status of an order by its order number    
def order_check(request):
    order = None
    order_num = request.GET.get('order_number', None)
    order_items = []
    if order_num:       
        try:
            order = Order.objects.get(id=order_num) # Fetch the order by ID
            order_items = OrderItem.objects.filter(order=order) # Fetch all order items for that order
        except:        
            order = None  # Set order to None if not found
            order_items = [] # Set order items to an empty list if not found
    
    order_dict = {'order': order, 'order_items': order_items}
    return render(request, 'order.html', order_dict)
        
# API view to retrieve, update, or delete order items, restricted to authenticated users     
class OrderItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    # GET request to fetch all order items for a specific order (identified by 'pk')
    def get(self, request, pk):
        user = request.user
        queryset = OrderItem.objects.filter(order = pk)
        serializer = OrderItemSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # DELETE request to delete an order, managers can delete any order, users cannot    
    def delete(self, request, pk):
        if request.user.groups.filter(name='managers').exists():
            Order.objects.filter(user = pk).delete()
            return Response()
        return Response()     
        