from django.contrib import admin
from django.urls import path
from .views import MenuItemListView, UserView

urlpatterns = [
    path('api/menu-items/', MenuItemListView.as_view(), name='menu_item_list'),
    path('api/users/users/me/', UserView.as_view(), name='users_users_me'),
]
