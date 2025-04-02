from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .utils import *
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

# OWNER VIEWS

# Shouldve maybe used a CBV but dont know how to properly make one rn
def store_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("owner_login"))

    current_user = request.user
    store_name = current_user.username
    current_store = Store.objects.get(store_name=store_name)
    store_products = Product.objects.filter(store__store_name=store_name)
    items_all = Item.objects.all()
    if check_bankrupt(request):
        delete_store(request)
        return render(request, "grocery/bankrupt_page.html", {
            "store_name": store_name,
        })


    if request.method == "POST":
        # gets the submit button clicked
        submit_button = request.POST.get("submit_button")

        #checks whether the add product form is submitted by checking the value of the submit button of the submitted form
        if submit_button == "add_product":
            # keep in mind request.POST always returns str
            chosen_item_string = request.POST["item_chooser"]
            quantity_field = request.POST["quantity_field"]
            saleprice_field = request.POST["saleprice_field"]
            costprice, item_id = chosen_item_string.split("|")
            item_id = int(item_id)
            selected_item = Item.objects.get(id=item_id)

            if product_valid(quantity_field, saleprice_field, current_store, selected_item):
                #converting from str to int and Decimal
                costprice_decimal = Decimal(costprice)
                quantity_int = int(quantity_field)
                saleprice_decimal = Decimal(saleprice_field)
                item_id = int(item_id)
                selected_item = Item.objects.get(id=item_id)
                total_costprice = costprice_decimal * quantity_int
                updated_budget_ap = current_store.budget - total_costprice
                updated_profit_ap = current_store.profit - total_costprice

                if not updated_budget_ap < 0:
                    try:
                        existing_product = Product.objects.get(quantity = quantity_int, sale_price = saleprice_decimal, item_info = selected_item)
                        # adding store to existing_product product logic    
                        existing_product.store.add(current_store)

                        # updating the store stuff(budget/profit) logic
                        current_store.budget = updated_budget_ap
                        current_store.profit = updated_profit_ap
                        current_store.save()
                        return HttpResponseRedirect(reverse("store_view"))

                    except ObjectDoesNotExist:
                        new_product = Product(
                            quantity= quantity_int,
                            sale_price= saleprice_decimal,
                            item_info= selected_item,
                            # store= current_store, this raised error since you cannot directly assign to a manytomany field and have to rather add stuff to it
                        )
                        new_product.save()
                        new_product.store.add(current_store) #adds a store to the manytomany field since you cannot add directly

                        # updating the store stuff(budget/profit) logic
                        current_store.budget = updated_budget_ap
                        current_store.profit = updated_profit_ap
                        current_store.save()
                        return HttpResponseRedirect(reverse("store_view"))

                else:
                    return render(request, "grocery/store_view.html", {
                        "error_message_ap": "Not Enough Budget",
                        "store_name": store_name,
                        "budget": current_store.budget,
                        "profit": current_store.profit,
                        "store_products": store_products,
                        "items_all": items_all,
                        "show_menu": True,
                        "add_menu_toggled": True,
                    })

            else:
                return render(request, "grocery/store_view.html", {
                    "error_message_ap": "Can't Add This Product",
                    "store_name": store_name,
                    "budget": current_store.budget,
                    "profit": current_store.profit,
                    "store_products": store_products,
                    "items_all": items_all,
                    "show_menu": True,
                    "add_menu_toggled": True,
                })

        if submit_button == "add_quantity":
            added_quantity = int(request.POST["quantity_field_increase"])
            current_productname = request.POST["item_name_quantity_increase"]
            current_item = items_all.get(item_name = current_productname)
            current_product = store_products.get(item_info= current_item.id)

            updated_quantity = int(current_product.quantity) + added_quantity 

            costprice_q = current_item.cost_price * added_quantity
            updated_budget_q = current_store.budget - costprice_q
            updated_profit_q = current_store.profit - costprice_q

            if updated_quantity <= 100:
                if not updated_budget_q < 0:
                    current_product.quantity = updated_quantity
                    current_product.save()

                    current_store.budget = updated_budget_q
                    current_store.profit = updated_profit_q
                    current_store.save()

                    return HttpResponseRedirect(reverse("store_view"))
                else:
                    return render(request, "grocery/store_view.html", {
                        "error_message_table": "Not Enough Budget",
                        "store_name": store_name,
                        "budget": current_store.budget,
                        "profit": current_store.profit,
                        "store_products": store_products,
                        "items_all": items_all,

                    })

            else:
                return render(request, "grocery/store_view.html", {
                    "error_message_table": "Quantity Cannot Exceed 100",
                    "store_name": store_name,
                    "budget": current_store.budget,
                    "profit": current_store.profit,
                    "store_products": store_products,
                    "items_all": items_all,

                })
                    
        if submit_button == "add_saleprice":
            new_saleprice = Decimal(request.POST["saleprice_field"])
            current_itemname = request.POST["item_name_change_saleprice"]
            current_item = items_all.get(item_name = current_itemname)
            current_product = store_products.get(item_info= current_item.id)

            if 1.00 <= new_saleprice <= 20.00:
                current_product.sale_price = new_saleprice
                current_product.save()
                return HttpResponseRedirect(reverse("store_view"))
            else:
                return render(request, "grocery/store_view.html", {
                    "error_message_table": "Unacceptable Saleprice",
                    "store_name": store_name,
                    "budget": current_store.budget,
                    "profit": current_store.profit,
                    "store_products": store_products,
                    "items_all": items_all,

                })


    return render(request, "grocery/store_view.html", {
        "store_name": store_name,
        "budget": current_store.budget,
        "profit": current_store.profit,
        "store_products": store_products,
        "items_all": items_all,
    })


def choose_role(request):
    return render(request, "grocery/choose_role.html", {
    })
    

def owner_login(request):
    if request.method == "POST":
        store_name = request.POST["storename"]
        password = request.POST["password"]
        user = authenticate(request, username=store_name, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("store_view"))
        else:
            return render(request, "grocery/owner_login.html", {
                "error_message": "Storename or Password is Incorrect"
            })
    return render(request, "grocery/owner_login.html")


def owner_signup(request):
    if request.method == "POST":
        store_name = request.POST["storename"]
        password = request.POST["password"]
        
        if store_valid(store_name, password):
            user = User.objects.create_user(username=store_name, password=password)
            user.save()
            store = Store(owner= User.objects.get(username= store_name), store_name=store_name)
            store.save()
            return HttpResponseRedirect(reverse("owner_login"))
        else:
            return render(request, "grocery/owner_signup.html",{
                "error_message": "Wrong Credentials"
            })
    return render(request, "grocery/owner_signup.html")


def owner_logout(request):
    logout(request)
    return render(request, "grocery/owner_login.html")


def store_leaderboard(request):
    # sorry for my long asf comments, hope they help future me understand the things in this code that i at the moment think are hard to write and wrap my head around at times

    stores_ranked_b = Store.objects.order_by('-budget')[:100]# .order_by('+budget') gets the stores in descending order based on budget while [:100] will filter top 100 stores
    stores_ranked_p = Store.objects.order_by('-profit')[:100]

    #these two give each instance from stores_ranked_b, and stores_ranked_p a temporary attribute called rank_b or rank_p
    for index, store in enumerate(stores_ranked_b, start=1): #enumerate returns an index(numbers of an ordered list in general, in this case the ranking of the stores since stores_ranked_b is sorted in descending order based on budget) and a value(in this case called store which is an istance of the Store model)
        store.rank_b = index #since store is an instance of the Store model/class, doing store.rank_b assigns a temporary variable/attribute called rank_b to the instance and that rank_b is equal to the index(in this case it is the ranking because stores_ranked_b is sorted in descending order based on budget)  

    for index, store in enumerate(stores_ranked_p, start=1):
        store.rank_p = index 

    return render(request, "grocery/store_leaderboard.html",{
        "stores_ranked_b": stores_ranked_b,
        "stores_ranked_p": stores_ranked_p,
        #if you are wondering why store.rank_b or store.rank_p is not passed into the template, the reason is that they do no need to be since they are not variables and rank_b/rank_p are attributes/variables assigned to instance "store" and the instances are already pased in the above two thingies
    })


def delete_store(request):
    current_user = request.user
    store_name = current_user.username
    current_store = Store.objects.get(store_name=store_name)

    # Remove current store from all related products
    current_store.product.clear()  # Clears all products related to the current store
    
    # Optionally delete products that are orphaned (i.e., no stores are associated)
    orphaned_products = Product.objects.filter(store__isnull=True)  # Get all products with no related stores
    orphaned_products.delete()  # Delete orphaned products

    current_user.delete()
    current_store.delete()
    messages.success(request, "Store deleted successfully.")
    return HttpResponseRedirect(reverse("owner_login"))
    

def delete_product(request, product_id):
    #refund
    product = Product.objects.get(id= product_id)

    current_user = request.user
    store_name = current_user.username
    current_store = Store.objects.get(store_name=store_name)

    refund_amount = product.item_info.cost_price * product.quantity
    updated_budget_r = current_store.budget + refund_amount
    updated_profit_r = current_store.profit + refund_amount

    current_store.budget = updated_budget_r
    current_store.profit = updated_profit_r
    current_store.save()


    # deletion
    product.delete()
    return HttpResponseRedirect(reverse("store_view"))


#CUSTOMER VIEWS

def browse_stores(request):
    all_stores = Store.objects.all()
    return render(request, "grocery/browse_stores.html", {
        "all_stores": all_stores,


    })

def visited_store(request, store_id):
    current_store = Store.objects.get(pk = store_id)
    store_products = Product.objects.filter(store= store_id)
    
    if request.method == "POST":
        # gets the submit button clicked
        submit_button = request.POST.get("submit_button")

        if submit_button == "submit_review":
            chosen_review = request.POST["select_review"]

            match chosen_review:
                case "very_good":
                    addition = Decimal(Decimal(2.5)/Decimal(100) * current_store.budget)
                    updated_budget = current_store.budget + addition
                    current_store.budget = updated_budget
                    current_store.save()
                    messages.success(request, "Thank You For Your Feedback", extra_tags="review_feedback_message")
                    return HttpResponseRedirect(reverse("visited_store", args=[current_store.id]))
                case "good":
                    addition = Decimal(Decimal(1)/Decimal(100) * current_store.budget)
                    updated_budget = current_store.budget + addition
                    current_store.budget = updated_budget
                    current_store.save()
                    messages.success(request, "Thank You For Your Feedback", extra_tags="review_feedback_message")
                    return HttpResponseRedirect(reverse("visited_store", args=[current_store.id]))
                case "bad":
                    subtraction = Decimal(Decimal(1)/Decimal(100) * current_store.budget)
                    updated_budget = current_store.budget - subtraction
                    current_store.budget = updated_budget
                    current_store.save()
                    messages.success(request, "Thank You For Your Feedback", extra_tags="review_feedback_message")
                    return HttpResponseRedirect(reverse("visited_store", args=[current_store.id]))
                case "very_bad":
                    subtraction = Decimal(Decimal(2.5)/Decimal(100) * current_store.budget)
                    updated_budget = current_store.budget - subtraction
                    current_store.budget = updated_budget
                    current_store.save()
                    messages.success(request, "Thank You For Your Feedback", extra_tags="review_feedback_message")
                    return HttpResponseRedirect(reverse("visited_store", args=[current_store.id]))
                case "terrible":
                    subtraction = Decimal(Decimal(5)/Decimal(100) * current_store.budget)
                    updated_budget = current_store.budget - subtraction
                    current_store.budget = updated_budget
                    current_store.save()
                    messages.success(request, "Thank You For Your Feedback", extra_tags="review_feedback_message")
                    return HttpResponseRedirect(reverse("visited_store", args=[current_store.id]))

        if submit_button == "submit_buy":
           quantity_bought = int(request.POST["quantity_field_buy"])
           product_bought_id = int(request.POST["product_id"])
           product_bought = Product.objects.get(pk=product_bought_id)

           if not quantity_bought > product_bought.quantity:
                if not quantity_bought <= 0:
                    cost = product_bought.sale_price * quantity_bought
                    updated_store_budget = current_store.budget + cost
                    updated_store_profit = current_store.profit + cost 
                    updated_product_quantity= product_bought.quantity - quantity_bought

                    current_store.budget = updated_store_budget
                    current_store.profit = updated_store_profit
                    product_bought.quantity = updated_product_quantity
                    current_store.save()
                    product_bought.save()
                    messages.success(request, "Item Purchased Successfully", extra_tags="item_bought_message")
                    return HttpResponseRedirect(reverse("visited_store", args=[current_store.id]))
               
                else:
                    return render(request, "grocery/visited_store.html", {
                        "current_store": current_store,
                        "store_products": store_products,
                        "error_message_q": "Quantity Bought Should be Greater than 0",
                    })

           else:
                return render(request, "grocery/visited_store.html", {
                    "current_store": current_store,
                    "store_products": store_products,
                    "error_message_q": "Not Enough Items",
                })    

            
    return render(request, "grocery/visited_store.html", {
        "current_store": current_store,
        "store_products": store_products,
    })


#EXTRAS

def check_bankrupt(request):
    current_user = request.user
    store_name = current_user.username
    current_store = Store.objects.get(store_name=store_name)
    store_products = Product.objects.filter(store__store_name=store_name)
    if current_store.budget < 20 and not store_products.exists():
        return True
    return False


    

