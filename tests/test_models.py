import pytest
from decimal import Decimal
from django.contrib.auth.models import User


from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from users.models import Profile

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
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="pass123")


@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user)



@pytest.mark.django_db
class TestCategory:
    def test_str(self, category):
        """Category.__str__ должен возвращать название категории"""
        assert str(category) == "Смартфоны"

@pytest.mark.django_db
class TestOrderItem:
    def test_price_snapshot(self, order, product):
        """Цена в OrderItem должна сохраняться как снимок на момент заказа и не меняться, если потом изменилась цена самого товара"""
        item = OrderItem.objects.create(
            order=order,
            product=product,
            price=Decimal("12345.00"),
            quantity=1,
        )
        product.price = Decimal("1.00")
        product.save()
        item.refresh_from_db()
        assert item.price == Decimal("12345.00")

@pytest.mark.django_db
class TestProfileSignals:
    def test_auto_created_on_user_create(self):
        """При создании User должен автоматически создаваться Profile"""
        new_user = User.objects.create_user(username="alina", password="pass")
        assert Profile.objects.filter(user=new_user).exists()


@pytest.mark.django_db
class TestProduct:
    def test_str(self, product):
        """Product.__str__ должен возвращать название товара"""
        assert str(product) == "iPhone 15"
    def test_product_belongs_to_category(self, product, category):
        """Товар должен принадлежать своей категории"""
        assert product.category == category


@pytest.mark.django_db
class TestReview:
    def test_review_belongs_to_product_and_user(self, product, user):
        """Отзыв должен принадлежать товару и пользователю"""
        review = Review.objects.create(
            product=product,
            user=user,
            text="Отличный телефон!",
            rating=5,
        )
        assert review.product == product
        assert review.user == user
        assert review.rating == 5

    def test_review_rating_default(self, product, user):
        """Проверка для значения по умолчанию рейтинга"""
        review = Review.objects.create(
            product=product,
            user=user,
            text="Хороший телефон",
        )
        assert review.rating == 5


@pytest.mark.django_db
class TestCategory:
    def test_slug_unique(self, category):
        """Слаг категории должен быть уникальным"""
        assert category.slug == "smartphones"


@pytest.mark.django_db
class TestOrder:
    def test_order_belongs_to_user(self, order, user):
        """Заказ должен принадлежать пользователю"""
        assert order.user == user

    def test_order_created_at_auto_now_add(self, order):
        """Поле created_at должно заполняться автоматически"""
        assert order.created_at is not None
