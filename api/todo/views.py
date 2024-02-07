from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.todo.serializers import TaskSerializer
from apps.todo.models import Task, TasksList


class TasksViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(tasks_list__user=self.request.user)
        return queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        tasks_list, created = TasksList.objects.get_or_create(user=user)
        serializer.save(tasks_list=tasks_list, is_completed=False)
