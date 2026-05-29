from django.urls import path, include
from . import views, api_views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('chat/', views.chat_room, name='chat_room'),

    # API
    path('api/categories/', api_views.CategoryListAPIView.as_view(), name='api_categories'),
    path('api/categories/<int:pk>/', api_views.CategoryDetailAPIView.as_view(), name='api_category_detail'),
    path('api/products/', api_views.ProductListAPIView.as_view(), name='api_products'),
    path('api/products/<int:pk>/', api_views.ProductDetailAPIView.as_view(), name='api_product_detail'),
]