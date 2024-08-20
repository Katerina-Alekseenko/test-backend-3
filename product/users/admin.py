from django.contrib import admin
from .models import CustomUser, Balance, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active")


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ("user", "amount")
    search_fields = ("user__email",)
    list_filter = ("amount",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "subscribed_at")
    search_fields = ("user__email", "course__title")
    list_filter = ("subscribed_at",)
