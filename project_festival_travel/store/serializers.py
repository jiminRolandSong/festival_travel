from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from .models import Category, Festival, Package, Order, OrderItem, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        
class FestivalSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Festival
        fields = ['id', 'category', 'name', 'slug', 'location', 'start_date', 'end_date', 'description']
        
class PackageSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    festival = FestivalSerializer(read_only=True)
    
    class Meta:
        model = Package
        fields = ['id', 'category', 'festival', 'name', 'slug', 'price',
                  'description', 'featured', 'availability']

class CartSerializer (serializers.ModelSerializer): 
    user = serializers.PrimaryKeyRelatedField( 
    queryset=User.objects.all(), 
    default=serializers.CurrentUserDefault(), 
    )
    
    package = serializers.PrimaryKeyRelatedField(
        queryset = Package.objects.all(),
    )
     
    class Meta:
        model = Cart
        fields = ['id','user','package', 'quantity', 'price']
        
class OrderSerializer (serializers.ModelSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Order
        fields = ['id','user', 'total_quantity', 'total_price', 'status', 'date']
        
class OrderItemSerializer (serializers.ModelSerializer):
    package = PackageSerializer()
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = OrderItem
        fields = ['id', 'user', 'package', 'quantity', 'price']