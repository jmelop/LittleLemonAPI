from django.contrib import admin
from django.urls import path
from .views import MenuItemListView

urlpatterns = [
    path('api/menu-items/', MenuItemListView.as_view(), name='menu_item_list'),
]
