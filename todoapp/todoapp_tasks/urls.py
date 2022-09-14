from django.urls import path

from .views import ListTasksView, GetTaskView, DeleteTaskView, TaskReorderView

urlpatterns = [
    path('', ListTasksView.as_view(), name='list_of_tasks'),
    path('<int:id>/', GetTaskView.as_view(), name='get_task_by_id'),
    path('delete/<int:id>/', DeleteTaskView.as_view(), name='delete_task_by_id'),
    path('reorder', TaskReorderView.as_view(), name='reorder_list_of_tasks'),
]
