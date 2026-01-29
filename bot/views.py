from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import TelegramUser
from .serializers import TelegramUserSerializer


@api_view(["GET"])
def api_root(request):
    """Корневой эндпоинт API с доступными маршрутами."""
    return Response({
        "register": reverse("register_user", request=request),
        "user": reverse("get_user", kwargs={"user_id": "<user_id>"}, request=request),
        "description": "Django REST API для Telegram-бота"
    })


@api_view(["POST"])
def register_user(request):
    """
    Регистрация пользователя Telegram.
    Идемпотентно: если пользователь существует, возвращает 200.
    """
    user_id = request.data.get("user_id")
    username = request.data.get("username")

    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user, created = TelegramUser.objects.get_or_create(
        user_id=user_id,
        defaults={"username": username}
    )

    serializer = TelegramUserSerializer(user)
    data = serializer.data

    if created:
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data["already_registered"] = True
        return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user(request, user_id: int):
    """
    Получение данных пользователя по user_id.
    """
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except TelegramUser.DoesNotExist:
        return Response(
            {"message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
