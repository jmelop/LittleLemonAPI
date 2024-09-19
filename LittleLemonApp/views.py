from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem
from .serializers import MenuItemSerializer
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