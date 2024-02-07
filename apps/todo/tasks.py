from collections import defaultdict
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now

from .models import Task


@shared_task
def send_expiring_tasks_reminders():
    today = now().date()
    coming_days = today + timedelta(days=3)

    tasks = (
        Task.objects.filter(due_date__range=[today, coming_days])
        .select_related("tasks_list__user")
        .order_by("due_date")
        .values("due_date", "description", "tasks_list__user__email")
    )

    user_tasks_info = defaultdict(list)
    for task in tasks:
        user_email = task["tasks_list__user__email"]
        user_tasks_info[user_email].append(task)

    for user_email, tasks_info in user_tasks_info.items():
        subject = f'Notification of tasks with the nearest due dates per {today.strftime("%m.%d.%Y")}'
        message_lines = [
            f"- Task {task['description']} - {task['due_date']}" for task in tasks_info
        ]
        message = "List of tasks with the nearest due dates:\n" + "\n".join(
            message_lines
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
