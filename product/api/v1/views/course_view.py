from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.v1.permissions import IsStudentOrIsAdmin, make_payment
from api.v1.serializers.course_serializer import (
    CourseSerializer,
    CreateCourseSerializer,
    CreateGroupSerializer,
    CreateLessonSerializer,
    GroupSerializer,
    LessonSerializer,
)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(
            Course,
            id=self.kwargs.get("course_id")
        )
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(
            Course,
            id=self.kwargs.get("course_id")
        )
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(
            Course,
            id=self.kwargs.get("course_id")
        )
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(
            Course,
            id=self.kwargs.get("course_id")
        )
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы"""

    queryset = Course.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=["post"], detail=True, permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk=None):
        """Покупка доступа к курсу (подписка на курс)."""

        course = self.get_object()
        try:
            subscription = make_payment(request, course.id)
            serializer = SubscriptionSerializer(subscription)
            data = {
                "subscription": serializer.data,
                "message": "Payment successful. Access granted to the course.",
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
