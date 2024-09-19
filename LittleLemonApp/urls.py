from django.contrib import admin
from django.urls import path
from .views import UserView, MenuItemView, MenuItemDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # API users
    path('api/users/users/me/', UserView.as_view(), name='users_users_me'),
    path('api/users', UserView.as_view(), name='users_users_me'),
    path('api/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API menu items
    path('api/menu-items', MenuItemView.as_view(), name='menu_item_list'),
    path('api/menu-items/<int:pk>', MenuItemDetailView.as_view(), name='menu_item_list'),
]
