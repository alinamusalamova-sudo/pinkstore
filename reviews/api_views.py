from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Review
from catalog.models import Product
from .serializers import ReviewSerializer, ReviewCreateUpdateSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    summary="Список отзывов",
    description="Возвращает список всех отзывов ко всем товарам",
    tags=['Отзывы']
)

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

@extend_schema(
    summary="Детальная информация об отзыве",
    description="Возвращает отзыв о его ID",
    tags=['Отзывы']
)

class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

@extend_schema(
    summary="Создание отзыва",
    description="Добавляет новый отзыв к товару",
    tags=['Отзывы'],
    request=ReviewCreateUpdateSerializer,
    responses={
        201: OpenApiResponse(description='Отзыв успешно создан'),
        400: OpenApiResponse(description='Ошибка валидации'),
        401: OpenApiResponse(description='Не авторизован'),
    }
)
class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product)


@extend_schema(
    summary="Обновление отзыва",
    description="Обновляет существующий отзыв",
    tags=['Отзывы'],
    request=ReviewCreateUpdateSerializer,
    responses={
        200: ReviewSerializer,
        400: OpenApiResponse(description='Ошибка валидации'),
        403: OpenApiResponse(description='Нельзя редактировать чужой отзыв'),
        404: OpenApiResponse(description='Отзыв не найден'),
    }
)
class ReviewUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ReviewCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


@extend_schema(
    summary="Удаление отзыва",
    description="Удаляет отзыв",
    tags=['Отзывы'],
    responses={
        204: OpenApiResponse(description='Отзыв успешно удален'),
        403: OpenApiResponse(description='Нельзя удалять чужой отзыв'),
        404: OpenApiResponse(description='Отзыв не найден'),
    }
)
class ReviewDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)