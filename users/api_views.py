from rest_framework import generics, permissions
from users.models import Profile
from .serializers import ProfileSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

@extend_schema(
    summary="Профиль текущего пользователя",
    description=("Возвращает профиль авторизованного пользователя: "
    "логин, email, телефон и адрес доставки. Требует аутентификации"
),
    tags=['Пользователи']
)

class MyProfileAPIView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)