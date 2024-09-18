from django.http import JsonResponse
from django.views import View
from .models import MenuItem, User

class MenuItemListView(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all().values()
        return JsonResponse(list(menu_items), safe=False, status=200)
    
    def __str__(self):
        return self.name

class UsersView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.all().values()
        return JsonResponse(list(user), safe=False, status=200)
    
    def __str__(self):
        return self.name