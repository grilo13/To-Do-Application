from django.urls import path

from .views import ListTasksView

urlpatterns = [
    path('', ListTasksView.as_view(), name='list_of_tasks')
]
