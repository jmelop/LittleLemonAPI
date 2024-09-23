from rest_framework import serializers
from .models import MenuItem, CartItem, Cart, OrderItem, Order
from django.contrib.auth import get_user_model

User = get_user_model()

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price']

class CartMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['menu_item', 'quantity']
    
    def create(self, validated_data):
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user)
        
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart,
            menu_item=validated_data['menu_item'],
            defaults={'quantity': validated_data['quantity']}
        )
        return cart_item


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items'] 
        
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
