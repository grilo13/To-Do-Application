from django.urls import path

from .views import ListTasksView, GetTaskView, DeleteTaskView, TaskReorderView, CreateTask, CompleteTask

urlpatterns = [
    path('', ListTasksView.as_view(), name='list_of_tasks'),
    path('create/', CreateTask.as_view(), name='create_task'),
    path('<int:id>/', GetTaskView.as_view(), name='get_task_by_id'),
    path('delete/<int:id>/', DeleteTaskView.as_view(), name='delete_task_by_id'),
    path('reorder', TaskReorderView.as_view(), name='reorder_list_of_tasks'),
    path('complete/<int:id>/', CompleteTask.as_view(), name='complete_task'),
]
