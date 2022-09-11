from django.urls import path

from .views import ListTasksView, GetTaskView

urlpatterns = [
    path('', ListTasksView.as_view(), name='list_of_tasks'),
    path('<int:id>/', GetTaskView.as_view(), name='get_task_by_id'),
]
