from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_list, name='shop_list'),
    path('category/<slug:category_slug>/', views.shop_list, name='shop_category'),

    # 👇 ТУТ ЗМІНА: використовуємо int:product_id замість slug
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<str:cart_key>/', views.cart_remove, name='cart_remove'),
]