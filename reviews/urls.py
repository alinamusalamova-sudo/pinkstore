from django.urls import path
from .views import review_list, add_review, edit_review, delete_review
from .import api_views, views

app_name = 'reviews'
urlpatterns = [
    path('all/', views.review_list, name='review_list'),
    path('product/<int:product_id>/add/', views.add_review, name='add_review'),
    path('<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('api/reviews/', api_views.ReviewListAPIView.as_view(), name='api_reviews'),
    path('api/reviews/<int:pk>/', api_views.ReviewDetailAPIView.as_view(), name='api_review_detail'),
    path('api/products/<int:product_id>/reviews/', api_views.ReviewCreateAPIView.as_view(), name='api_review_create'),
    path('api/reviews/<int:pk>/update/', api_views.ReviewUpdateAPIView.as_view(), name='api_review_update'),
    path('api/reviews/<int:pk>/delete/', api_views.ReviewDeleteAPIView.as_view(), name='api_review_delete'),
]