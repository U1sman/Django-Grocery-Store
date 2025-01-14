from django.contrib import admin
from .models import *

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "cost_price")


class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "store_name", "budget", "profit")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "quantity", "sale_price", "item_info")



admin.site.register(Item, ItemAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
