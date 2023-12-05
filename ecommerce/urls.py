from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('view_page/<str:name>/', views.view, name="view_page"),
    path('profile', views.profile, name="profile"),
    path('profile/edit_user_info', views.editUserInfo, name="edit_user_info"),
    path("wishlist/", views.add_to_wishlist, name="wishlist"),

    path('update_item/', views.updateItem, name="update_item"),
    path('update_wishlist/', views.updateWishList, name="update_wishlist"),
    # path('delete_wishlist/', views.deleteWishList, name="delete_wishlist"),
    path('process_order/', views.processOrder, name="process_order"),
]