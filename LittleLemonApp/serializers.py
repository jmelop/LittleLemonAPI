from rest_framework import serializers
from .models import MenuItem, CartItem, Cart, OrderItem, Order, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'unit_price', 'featured']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CartMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['menuitem', 'quantity', 'unit_price']
    
    def create(self, validated_data):
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user)
        
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart,
            menuitem=validated_data['menuitem'],
            defaults={'quantity': validated_data['quantity'], 'unit_price': validated_data['unit_price']}
        )
        return cart_item


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'items'] 
        read_only_fields = ['id', 'user', 'created_at']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            email = validated_data['email'],
            password = password
        )
        return user
