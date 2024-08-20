from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import Subscription, Balance
from courses.models import Course

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password"
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    def create(self, validated_data):
        user = validated_data["user"]
        course = validated_data["course"]

        # Проверка баланса пользователя
        balance = Balance.objects.get(user=user)
        if balance.amount < course.price:
            raise ValidationError(
                "Insufficient balance to purchase the course."
            )

        # Списание бонусов с баланса пользователя
        balance.amount -= course.price
        balance.save()

        # Создание подписки
        subscription = Subscription.objects.create(
            user=user,
            course=course
        )

        return subscription

    class Meta:
        model = Subscription
        fields = ("id", "user", "course", "subscribed_at")
        read_only_fields = ("id", "subscribed_at")
