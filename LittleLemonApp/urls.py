from django.contrib import admin
from django.urls import path
from .views import MenuItemListView, UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # API users
    path('api/users/users/me/', UserView.as_view(), name='users_users_me'),
    path('api/users', UserView.as_view(), name='users_users_me'),
    path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API menu items
    path('api/menu-items/', MenuItemListView.as_view(), name='menu_item_list'),
]
