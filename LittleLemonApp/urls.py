from django.contrib import admin
from django.urls import path
from .views import MenuItemListView, UserView

urlpatterns = [
    # API users
    path('api/users/users/me/', UserView.as_view(), name='users_users_me'),
    path('api/users', UserView.as_view(), name='users_users_me'),
    path('token/login/', UserView.as_view(), name='users_users_me'),
    # API menu items
    path('api/menu-items/', MenuItemListView.as_view(), name='menu_item_list'),
]
