import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from catalog.models import Category, Product

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category(db):
    return Category.objects.create(name="Смартфоны", slug="smartphones")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        title="iPhone 15",
        description="Крутой телефон",
        price=Decimal("99999.99"),
        stock=10,
        is_available=True,
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        password="pass123",
        email="alice@example.com"
    )

@pytest.mark.django_db
def test_products_api_returns_list(api_client, product):
    """API списка товаров должен вернуть 200 и список с товарами"""
    # 1. Получаем URL по имени маршрута
    url = reverse('catalog:api_products')
    # 2. Отправляем GET-запрос к API
    response = api_client.get(url)
    # 3. Проверяем, что эндпоинт вообще работает и вернул 200 OK
    assert response.status_code == 200
    # 4. Разбираем JSON-ответ и проверяем полезные данные
    data = response.json()
    assert len(data) == 1  # мы создали ровно один товар в фикстуре
    assert data[0]['title'] == 'iPhone 15'
    assert data[0]['price'] == '99999.99'

@pytest.mark.django_db
def test_api_me_returns_profile_for_authenticated_user(api_client, user):
    """Авторизованный пользователь должен получить свой профиль"""
    # 1. Говорим клиенту считать все запросы от имени этого пользователя
    api_client.force_authenticate(user=user)
    # 2. Строим URL до эндпоинта /api/me/
    url = reverse('users:api_my_profile')
    # 3. Делаем запрос
    response = api_client.get(url)
    # 4. Проверяем статус — должен быть 200 OK
    assert response.status_code == 200
    # 5. Разбираем JSON и смотрим, что вернулся именно наш пользователь
    data = response.json()
    assert data['user']['username'] == user.username
    assert 'phone' in data
    assert 'address' in data


@pytest.mark.django_db
def test_categories_list(api_client, category):
    """Должен возвращать список категорий"""
    url = reverse('catalog:api_categories')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]['name'] == "Смартфоны"


@pytest.mark.django_db
def test_reviews_list(api_client, product, user):
    """Должен возвращать список отзывов"""
    from reviews.models import Review
    Review.objects.create(
        product=product,
        user=user,
        text="Отличный телефон!",
        rating=5,
    )
    url = reverse('reviews:api_reviews')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]['text'] == "Отличный телефон!"


@pytest.mark.django_db
def test_orders_list(api_client, user):
    """Должен возвращать список заказов"""
    api_client.force_authenticate(user=user)
    url = reverse('orders:api_orders')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.django_db
def test_product_detail_returns_correct_data(api_client, product, category):
    """Должен возвращать детали товара с вложенной категорией"""
    url = reverse('catalog:api_product_detail', kwargs={'pk': product.id})
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "iPhone 15"
    assert data['price'] == "99999.99"
    assert 'category' in data
    assert isinstance(data['category'], dict)
    assert data['category']['name'] == category.name
    assert data['category']['slug'] == category.slug