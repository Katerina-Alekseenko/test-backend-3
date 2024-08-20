from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name="Адрес электронной почты", max_length=250, unique=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name", "password")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-id",)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        CustomUser, related_name="balance", on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=1000, verbose_name="Баланс"
    )

    class Meta:
        verbose_name = "Баланс"
        verbose_name_plural = "Балансы"
        ordering = ("-id",)

    def __str__(self):
        return f"{self.user.email} - {self.amount}"


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser, related_name="subscriptions", on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        "courses.Course",
        related_name="subscriptions",
        on_delete=models.CASCADE
    )

    subscribed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата подписки"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("-id",)

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
