from rest_framework import generics
from orders.models import Order
from .serializers import OrderSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Список заказов",
    description="Возвращает список всех заказов с товарами и статусом оплаты",
    tags=['Заказы']
)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@extend_schema(
    summary="Детальная информация о заказе",
    description="Возвращает один заказ по erd ID, включая вложенные позиции (товары)",
    tags=['Заказы']
)

class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer