from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from .models import MenuItem
from .serializers import MenuItemSerializer, UserSerializer
from .permissions import IsManager, IsCustomerOrDeliveryCrew

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
    
    def get(self, request, *args, **kwargs):
        if IsCustomerOrDeliveryCrew().has_permission(request, self) or IsManager().has_permission(request, self):
            menu_items = MenuItem.objects.all()
            serializer = MenuItemSerializer(menu_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
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