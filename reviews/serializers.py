from reviews.models import Review
from catalog.models import Product
from django.contrib.auth.models import User
from rest_framework import serializers

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    product = ProductShortSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'user', 'product']

class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text', 'rating']