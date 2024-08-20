from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        course = instance.course
        groups = course.groups.all()
        if groups:
            least_filled_group = min(groups, key=lambda g: g.students.count())
            least_filled_group.students.add(instance.user)
