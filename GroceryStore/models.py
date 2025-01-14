from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator, MaxValueValidator
from decimal import Decimal
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=100)
    cost_price = models.DecimalField(decimal_places=2, max_digits=3, validators=[MinValueValidator(2.00), MaxValueValidator(5.00)])
    def __str__(self):
        return f"ITEM: {self.item_name}, COST_PRICE:{self.cost_price}" 
    

class Store(models.Model):
    owner = models.OneToOneField(User, on_delete= models.CASCADE, related_name="store")
    store_name = models.CharField(max_length=50, validators=[MinLengthValidator(10)])
    budget = models.DecimalField(decimal_places=2, max_digits=10, default=1000.00, validators=[MinValueValidator(20.00)])
    profit = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    def __str__(self):
        return f"STORE: {self.owner.username}" 


class Product(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sale_price = models.DecimalField(decimal_places=2, max_digits=4, validators=[MinValueValidator(1.00), MaxValueValidator(20.00)])
    item_info = models.ForeignKey(Item, on_delete=models.CASCADE) #this was previously OneToOneField but that was a problem since it enforced that each Item can only be associated with one Product. This means that for each Item, only one Product can exist in the database. If you're trying to associate multiple products with the same item (e.g., different quantities or sale prices), this will cause issues.
    store = models.ManyToManyField(Store, related_name="product")
    def __str__(self):
        return f"PRODUCT: {self.item_info.item_name}, SALE_PRICE: {self.sale_price}" 
    

#Nvm I add similar logic to the delete_store view to manually check the same thing since this signal thing wasnt working as expected, this was a waste of time

#I kinda understand how this works but not fully, chatgpt wrote it, will look into django signals like this later, this is a temporary fix    
# This is a signal that is fired whenever a change (adding or removing) is made to the "store" 
# ManyToManyField in the Product model.
# It checks if the product instance is orphaned (i.e., has no associated stores) after the change.
# If the product is orphaned (has no stores), it will be deleted.
# The signal fires for both "post_add" (when stores are added) and "post_remove" (when stores are removed).
# It also uses "instance.refresh_from_db()" to ensure the instance reflects the latest changes before checking.
# @receiver(m2m_changed, sender=Product.store.through)
# def check_product_stores(sender, instance, action, **kwargs):
#     if action == "post_remove":
#         instance.refresh_from_db()  # Refresh the product instance to get the latest state of related stores
#         if not instance.store.exists():  # Trigger after a store is removed
#             instance.delete()



 