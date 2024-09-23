from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from .models import MenuItem, Cart, CartItem, Order, OrderItem
from .serializers import MenuItemSerializer, UserSerializer, CartMenuItemSerializer, OrderItemSerializer, OrderSerializer
from .permissions import IsDeliveryCrew, IsManager, IsCustomerOrDeliveryCrew, IsCustomer

class UserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        self.permission_classes = [AllowAny]
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuItemView(generics.ListAPIView, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'price']
    ordering_fields = ['name', 'price']
    ordering = ['name']
    
    def get(self, request, *args, **kwargs):
            if IsCustomerOrDeliveryCrew().has_permission(request, self) or IsManager().has_permission(request, self):
                return super().get(request, *args, **kwargs)
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                menuItem = serializer.save()
                return Response(MenuItemSerializer(menuItem).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
class MenuItemDetailView(generics.RetrieveAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get(self, request, *args, **kwargs):
        if IsCustomerOrDeliveryCrew().has_permission(request, self) or IsManager().has_permission(request, self):
            return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            return self.partial_update(request, *args, **kwargs)
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    def put(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            return self.update(request, *args, **kwargs)
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            return self.destroy(request, *args, **kwargs)
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
class ManagerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            try:
                managers_group = Group.objects.get(name="Manager")
            except Group.DoesNotExist:
                return Response({"detail": "Manager group not found."}, status=404)
            
            managers = managers_group.user_set.all()
            managers_data = [
                {"id": user.id, "username": user.username, "email": user.email} for user in managers
            ]
            
            return Response(managers_data, status=200)
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            try:
                manager_group = Group.objects.get(name="Manager")
            except Group.DoesNotExist:
                return Response({"detail": "Manager group not found."}, status=404)
            
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            user.groups.add(manager_group)
            return Response({"detail": f"User {user.username} added to Manager group."}, status=status.HTTP_201_CREATED)
        
    def delete(self, request, user_id, *args, **kwargs):
        if IsManager().has_permission(request, self):
            try:
                manager_group = Group.objects.get(name="Manager")
            except Group.DoesNotExist:
                return Response({"detail": "Manager group not found."}, status=404)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            user.groups.remove(manager_group)
            return Response({"detail": f"User {user.username} removed to Manager group."}, status=status.HTTP_200_OK)

class DeliveryCrewListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            try:
                delivery_crew_group = Group.objects.get(name="Delivery Crew")
            except Group.DoesNotExist:
                return Response({"detail": "Delivery Crew group not found."}, status=404)
            
            delivery_crew_group = delivery_crew_group.user_set.all()
            delivery_crew_group_data = [
                {"id": user.id, "username": user.username, "email": user.email} for user in delivery_crew_group
            ]
            
            return Response(delivery_crew_group_data, status=200)
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            try:
                delivery_crew = Group.objects.get(name="Delivery crew")
            except Group.DoesNotExist:
                return Response({"detail": "Delivery crew group not found."}, status=404)
            
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            user.groups.add(delivery_crew)
            return Response({"detail": f"User {user.username} added to Delivery crew group."}, status=status.HTTP_201_CREATED)
        
    def delete(self, request, user_id, *args, **kwargs):
        if IsManager().has_permission(request, self):
            try:
                delivery_crew = Group.objects.get(name="Delivery crew")
            except Group.DoesNotExist:
                return Response({"detail": "Delivery crew group not found."}, status=404)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            user.groups.remove(delivery_crew)
            return Response({"detail": f"User {user.username} removed to Delivery crew group."}, status=status.HTTP_200_OK)
        
class CartMenuItemsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartMenuItemSerializer

    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            serializer = CartMenuItemSerializer(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)

        if cart_items.exists():
            cart_items.delete()
            return Response({'detail': 'All items deleted from the cart.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No items found in the cart.'}, status=status.HTTP_404_NOT_FOUND)

class OrderMenuItemsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif IsCustomerOrDeliveryCrew().has_permission(request, self):
                orders = Order.objects.filter(user=request.user)
                serializer = OrderItemSerializer(orders, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, *args, **kwargs):
        if IsCustomer().has_permission(request, self):
            user = request.user
            cart = Cart.objects.filter(user=user).first()
            if not cart or not cart.items.exists():
                return Response({"detail": "No items in the cart."}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.create(user=user)
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    quantity=cart_item.quantity
                )
            cart.items.all().delete()
            return Response({"detail": "Order created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

class OrderItemDetailView(generics.RetrieveAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get(self, request, order_id, *args, **kwargs):
        if IsCustomer().has_permission(request, self):
            try:
                order_item = Order.objects.get(id=order_id)
                if order_item.order.user != request.user:
                    return Response({"detail": "Order does not belong to the current user."},
                                    status=status.HTTP_403_FORBIDDEN)
                serializer = self.get_serializer(order_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except OrderItem.DoesNotExist:
                return Response({"detail": "Order item not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    
    def put(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        if IsManager().has_permission(request, self):
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        if IsManager().has_permission(request, self):
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if IsDeliveryCrew().has_permission(request, self):
            if 'status' in request.data and request.data['status'] in [0, 1]:
                serializer = OrderSerializer(order, data={'status': request.data['status']}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Invalid or missing status."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, order_id, *args, **kwargs):
        if IsManager().has_permission(request, self):
            try:
                order = Order.objects.get(id=order_id)
                order.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Order.DoesNotExist:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
