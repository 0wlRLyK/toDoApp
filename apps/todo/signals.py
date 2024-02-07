from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TasksList

User = get_user_model()


@receiver(post_save, sender=User)
def create_tasks_list_for_new_user(sender, instance: User, created, **kwargs):
    if created:
        TasksList.objects.create(user=instance)
