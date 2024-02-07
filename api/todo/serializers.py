from datetime import date

from django.utils import timezone
from rest_framework import serializers

from apps.todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {
            "tasks_list": {"read_only": True},
        }

    def validate_due_date(self, value: date):
        if value < timezone.now().date():
            raise serializers.ValidationError("The date must be no earlier than today")
        return value
