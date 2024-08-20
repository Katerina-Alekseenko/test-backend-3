from django.contrib import admin
from .models import Course, Lesson, Group


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "start_date", "price")
    search_fields = ("title", "author")
    list_filter = ("start_date",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "link")
    search_fields = ("title", "course__title")
    list_filter = ("course",)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    search_fields = ("title", "course__title")
    list_filter = ("course",)
