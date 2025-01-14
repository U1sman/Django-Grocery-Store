from django.urls import path
from . import views


urlpatterns = [
    path("", views.choose_role, name="choose_role"),
    path("store_view/", views.store_view, name="store_view"),

    path("owner_login/", views.owner_login, name="owner_login"),
    path("owner_signup/", views.owner_signup, name="owner_signup"),
    path("logout", views.owner_logout, name="owner_logout"),

    path("delete_store/", views.delete_store, name="delete_store"),
    path("delete_product/<int:product_id>/", views.delete_product, name="delete_product"),

    path("store_leaderboard/", views.store_leaderboard, name="store_leaderboard"),

    path("browse_stores/", views.browse_stores, name="browse_stores"),
    path("visited_store/<int:store_id>", views.visited_store, name="visited_store"),
]