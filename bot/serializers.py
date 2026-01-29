from rest_framework import serializers
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ["user_id", "username", "created_at"]
        read_only_fields = ["created_at"]
