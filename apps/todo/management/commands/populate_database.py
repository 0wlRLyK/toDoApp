import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import QuerySet
from django.utils.timezone import now

from apps.todo.models import Task, TasksList

User = get_user_model()


class Command(BaseCommand):
    help = "Populates the database with test data"
    username = "test_user"
    email_template = "{}@example.com"

    def _validate(self):
        if User.objects.filter(
            username__icontains=self.username, email__icontains=self.username
        ):
            raise CommandError("Database already populated")

    def _create_users(self):
        # In this case, objects are created one by one
        # instead of using bulk_create in order for the TaskList creation signal to be triggered.
        for number in range(5):
            username = f"{self.username}{number}"
            user = User.objects.create(
                username=username, email=self.email_template.format(username)
            )
            user.set_password("test")
            user.save()
        return User.objects.all()

    @staticmethod
    def _generate_random_date():
        start_date = now().date()
        end_of_year = datetime(year=start_date.year, month=12, day=31).date()
        delta = end_of_year - start_date
        random_number_of_days = random.randrange(delta.days + 1)
        return start_date + timedelta(days=random_number_of_days)

    @staticmethod
    def _generate_tasks_for_users(users: QuerySet[User]):
        tasks_to_create = []
        for user in users:
            tasks_list, _ = TasksList.objects.get_or_create(user=user)

            for category in Task.Categories.choices:
                for _ in range(5):
                    task = Task(
                        tasks_list=tasks_list,
                        description=f"Task for {category[1]}",
                        category=category[0],
                        due_date=Command._generate_random_date(),
                        is_completed=random.choice([True, False]),
                    )
                    tasks_to_create.append(task)
        Task.objects.bulk_create(tasks_to_create)

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                Command._generate_tasks_for_users(self._create_users())
        except Exception as e:
            raise CommandError(
                f"🟥 The next error occurred when filling the database with test data: {str(e)}"
            )
        self.stdout.write(
            self.style.SUCCESS("✅ The database is successfully populated")
        )
