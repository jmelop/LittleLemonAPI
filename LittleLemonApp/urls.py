from django.contrib import admin
from django.urls import path
from .views import MenuItemListView, UsersView

urlpatterns = [
    path('api/menu-items/', MenuItemListView.as_view(), name='menu_item_list'),
    path('api/users/users/me/', UsersView.as_view(), name='users_users_me'),
]
