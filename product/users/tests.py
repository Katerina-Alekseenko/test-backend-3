from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Balance, Subscription
from courses.models import Course

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from api.v1.serializers.user_serializer import (
    CustomUserSerializer,
    SubscriptionSerializer,
)

User = get_user_model()


class CustomUserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpass"))


class BalanceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )

    def test_balance_creation(self):
        balance = Balance.objects.create(user=self.user, amount=1000)
        self.assertEqual(balance.user, self.user)
        self.assertEqual(balance.amount, 1000)


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        self.course = Course.objects.create(
            author="Test Author",
            title="Test Course",
            start_date="2024-01-01T00:00:00Z",
            price=100,
            available=True,
        )

    def test_subscription_creation(self):
        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)
        self.assertIsNotNone(subscription.subscribed_at)


class UserViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="testadmin",
            email="testadmin@example.com",
            password="testpass"
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_list_users(self):
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CourseViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            author="Test Author",
            title="Test Course",
            start_date="2024-01-01T00:00:00Z",
            price=100,
            available=True,
        )
        self.balance = Balance.objects.create(user=self.user, amount=1000)

    def test_list_courses(self):
        url = reverse("courses-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_pay_for_course(self):
        url = reverse("courses-pay", args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course).exists()
        )
        self.assertEqual(Balance.objects.get(user=self.user).amount, 900)

    def test_pay_for_course_insufficient_balance(self):
        self.balance.amount = 50
        self.balance.save()
        url = reverse("courses-pay", args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course).exists()
        )


class CustomUserSerializerTest(APITestCase):
    def test_user_serialization(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        serializer = CustomUserSerializer(user)
        data = serializer.data
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "testuser@example.com")

    def test_user_deserialization(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass",
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpass"))


class SubscriptionSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        self.course = Course.objects.create(
            author="Test Author",
            title="Test Course",
            start_date="2024-01-01T00:00:00Z",
            price=100,
            available=True,
        )
        self.balance = Balance.objects.create(user=self.user, amount=1000)

    def test_subscription_serialization(self):
        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )
        serializer = SubscriptionSerializer(subscription)
        data = serializer.data
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(data["course"], self.course.id)
        self.assertIsNotNone(data["subscribed_at"])

    def test_subscription_deserialization(self):
        data = {"user": self.user.id, "course": self.course.id}
        serializer = SubscriptionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        subscription = serializer.save()
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)
        self.assertIsNotNone(subscription.subscribed_at)
