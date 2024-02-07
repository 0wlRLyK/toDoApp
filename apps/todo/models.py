from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TasksList(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="tasks_list"
    )

    def __str__(self):
        return f"{self.user.username} tasks list"


class Task(models.Model):
    class Categories(models.TextChoices):
        WORK = "work", "Work"
        PRIVATE = "private", "Private"
        LEARNING = "learning", "Learning"

    tasks_list = models.ForeignKey(
        TasksList, on_delete=models.CASCADE, related_name="tasks"
    )
    description = models.TextField(max_length=200)
    category = models.CharField(max_length=20, choices=Categories.choices)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk} - {self.description}"
