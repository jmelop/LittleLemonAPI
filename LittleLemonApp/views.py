from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer, UserSerializer
from .permissions import IsManager, IsCustomerOrDeliveryCrew

class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.user.groups.filter(name='Manager').exists():
            self.permission_classes = [IsAuthenticated, IsManager]
        else:
            self.permission_classes = [IsAuthenticated, IsCustomerOrDeliveryCrew]
        return super(MenuItemListView, self).get_permissions()
    
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
        