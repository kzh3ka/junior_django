from django.conf import settings
from django.db import models


class TaskStatus:
    OPEN = "open"
    CLOSED = "closed"

    CHOICHES = (
        (OPEN, "Открыта"),
        (CLOSED, "Закрыта"),
    )


class Task(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE
    )
    description = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=TaskStatus.CHOICHES, default=TaskStatus.OPEN, max_length=20)


class Watcher(models.Model):
    task = models.ForeignKey("todo.Task", null=False, on_delete=models.CASCADE, related_name="watcher")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, related_name="watched_tasks"
    )
