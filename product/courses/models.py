from django.db import models
from django.conf import settings


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name="Автор",
    )
    title = models.CharField(
        max_length=250,
        verbose_name="Название",
    )
    start_date = models.DateTimeField(
        auto_now=False, auto_now_add=False,
        verbose_name="Дата и время начала курса"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )

    available = models.BooleanField(
        default=True,
        verbose_name="Доступен"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("-id",)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name="Название",
    )
    link = models.URLField(
        max_length=250,
        verbose_name="Ссылка",
    )

    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ("id",)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        max_length=250,
        verbose_name="Название"
    )

    course = models.ForeignKey(
        Course,
        related_name="groups",
        on_delete=models.CASCADE
    )

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="course_groups",
        blank=True
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ("-id",)
