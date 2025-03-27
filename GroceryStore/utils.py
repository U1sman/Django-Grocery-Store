from django.contrib.auth.models import User
from decimal import Decimal
from .models import *


def store_valid(store_name, password):
    if store_name and password and 10 <= len(store_name) <= 50 and 8 <= len(password) <= 64 and not User.objects.filter(username=store_name).exists():
        return True
    return False

def product_valid(quantity_field, saleprice_field, current_store, selected_item):
    if not saleprice_field == "" and not quantity_field == "":
        try:
            quantity_float = float(quantity_field)
            saleprice_decimal = Decimal(saleprice_field)
            
            if quantity_float.is_integer() and 1 <= int(quantity_float) <= 100 and 1.00 <= saleprice_decimal <= 20.00 and not Product.objects.filter(item_info=selected_item, store= current_store).exists():
                return True
            else:
                return False  
        except ValueError:
            return False
    return False