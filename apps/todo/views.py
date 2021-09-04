from django import http
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Task, Watcher, TaskStatus
from .forms import TaskForm


TASK_FIELDS = "id", "description", "status", "owner__email"


def preview_instance(source):
    watcher_queryset = Watcher.objects.filter(task_id=source["id"]).select_related("user")
    watcher = list(map(
        preview_watcher,
        watcher_queryset.values("user__email")
    ))
    return {
        "id": source["id"],
        "description": source["description"],
        "status": source["status"],
        "watcher": watcher,
        "owner": {
            "email": source["owner__email"]
        },
    }


def preview_watcher(source):
    return {
        "email": source["user__email"]
    }


class TaskView(View):
    def get(self, _):
        queryset = Task.objects.select_related("owner")
        return http.JsonResponse(
            map(preview_instance, queryset.values(*TASK_FIELDS)),
            safe=False
        )

    def post(self, request):
        form = TaskForm(request.POST)
        if not form.is_valid():
            return http.HttpResponseBadRequest(form.errors)

        cleaned_data = form.cleaned_data

        instance = Task.objects.create(
            description=cleaned_data["description"],
            owner=request.user,
        )

        watcher_ids = request.POST.getlist("watchers")
        for watcher_id in map(int, watcher_ids):
            if watcher_id == request.user.id:
                return http.HttpResponseBadRequest("User can't watch own task")
            Watcher.objects.create(
                task_id=instance.id,
                user_id=watcher_id,
            )
        queryset = Task.objects.select_related("owner")
        instance = get_object_or_404(queryset.values(*TASK_FIELDS), id=instance.id)
        return http.JsonResponse(preview_instance(instance))


class TaskDetailView(View):
    def get(self, _, pk):
        queryset = Task.objects.select_related("owner")
        instance = get_object_or_404(queryset.values(*TASK_FIELDS), id=pk)
        return http.JsonResponse(preview_instance(instance))


class TaskCloseView(View):
    def post(self, _, pk):
        queryset = Task.objects.select_related("owner")
        instance = get_object_or_404(queryset.values(*TASK_FIELDS), id=pk)
        if instance["status"] == TaskStatus.CLOSED:
            return http.HttpResponseBadRequest("Can't close alredy closed task")
        Task.objects.filter(id=pk).update(status=TaskStatus.CLOSED)
        return http.JsonResponse(preview_instance(instance))


class WatcherView(View):
    def get(self, _, pk):
        watcher_queryset = Watcher.objects.filter(task_id=pk).select_related("user")
        watcher = list(map(
            preview_watcher,
            watcher_queryset.values("user__email")
        ))
        return http.JsonResponse(watcher, safe=False)
