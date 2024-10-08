from django.contrib import admin
from django.urls import path
from .views import UserView, MenuItemView, MenuItemDetailView, ManagerListView, DeliveryCrewListView, CartMenuItemsView, OrderMenuItemsView, OrderItemDetailView, CategoryListCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # API users
    path('api/users/users/me/', UserView.as_view(), name='users_users_me'),
    path('api/users', UserView.as_view(), name='users_users_me'),
    path('auth/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API categories
    path('api/categories', CategoryListCreateView.as_view(), name='category_list'),
    # API menu items
    path('api/menu-items', MenuItemView.as_view(), name='menu_item_list'),
    path('api/menu-items/<int:pk>', MenuItemDetailView.as_view(), name='menu_item_list'),
    # API groups manager users
    path('api/groups/manager/users', ManagerListView.as_view(), name='manager_list_view'),
    path('api/groups/manager/users/<int:user_id>', ManagerListView.as_view(), name='manager_list_view'),
    path('api/groups/delivery-crew/users', DeliveryCrewListView.as_view(), name='delivery-crew_list_view'),
    path('api/groups/delivery-crew/users/<int:user_id>', DeliveryCrewListView.as_view(), name='delivery-crew_list_view'),
    # API cart management
    path('api/cart/menu-items', CartMenuItemsView.as_view(), name='cart_menu_items_view'),
    # API order management
    path('api/cart/orders', OrderMenuItemsView.as_view(), name='order_menu_items_view'),
    path('api/cart/orders/<int:order_id>', OrderItemDetailView.as_view(), name='order_menu_items_view'),
]
