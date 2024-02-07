import django_filters

from apps.todo.models import Task


class TaskFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(
        field_name="category", choices=Task.Categories.choices
    )
    is_completed = django_filters.BooleanFilter(field_name="is_completed")

    class Meta:
        model = Task
        fields = ["category", "is_completed"]
