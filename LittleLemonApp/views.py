from django.http import JsonResponse
from django.views import View
from .models import MenuItem

class MenuItemListView(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all().values()
        return JsonResponse(list(menu_items), safe=False, status=200)
    
    def __str__(self):
        return self.name