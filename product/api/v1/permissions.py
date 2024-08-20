from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription, Balance
from courses.models import Course
from rest_framework.exceptions import ValidationError


def make_payment(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)

    # Проверка баланса пользователя
    balance = Balance.objects.get(user=user)
    if balance.amount < course.price:
        raise ValidationError("Insufficient balance to purchase the course.")

    # Списание бонусов с баланса пользователя
    balance.amount -= course.price
    balance.save()

    # Создание подписки
    subscription = Subscription.objects.create(user=user, course=course)

    return subscription


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class ReadOnlyOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
