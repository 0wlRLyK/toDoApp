from django.urls import path

from api.todo.views import TasksViewSet

app_name = "todo"
urlpatterns = [
    path("", TasksViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "<int:pk>/",
        TasksViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
]
