from django.urls import path

from . import views


urlpatterns = [
    path("task/", views.TaskView.as_view()),
    path("task/<int:pk>/", views.TaskDetailView.as_view()),
    path("task/<int:pk>/close/", views.TaskCloseView.as_view()),
    path("task/<int:pk>/watcher/", views.WatcherView.as_view()),
]
