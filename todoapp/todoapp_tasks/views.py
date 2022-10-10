from django.shortcuts import render, redirect, reverse
from rest_framework.views import APIView

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.db.models.query import QuerySet

# Response
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Models
from .models import ToDoTask
from todoapp.todoapp_users.models import User

# Serializers
from .serializers import TaskSerializer


# Create your views here.
class ListTasksView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ToDoTask.objects.all()

    def get(self, request):
        user = request.user
        tasks = ToDoTask.objects.filter(user=user)
        context = {'tasks': tasks, 'count': tasks.count()}
        return render(request, 'task_list.html', context)


class CreateTask(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ToDoTask.objects.all()

    def get(self, request):
        return render(request, 'create_task.html')

    def post(self, request):
        user = request.user
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
        else:
            return Response(serializer.errors)

        return redirect('list_of_tasks')


class GetTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ToDoTask.objects.all()

    def get(self, request, id):
        user = request.user
        task = ToDoTask.objects.get(user=user, id=id)
        context = {'task': task}
        return render(request, 'task_object.html', context)


class UpdateTaskView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        user = request.user
        data = request.data
        task_description = data.get('description')

        try:
            task = ToDoTask.objects.get(user=user, id=id)
            task.description = task_description
            task.save(update_fields=['description'])
        except Exception as e:
            # return render(request, 'task_object.html', {'error': 'Something went wrong.'})
            return redirect('list_of_tasks')

        context = {'message': 'Description update successfully.'}
        return redirect('list_of_tasks')


class DeleteTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ToDoTask.objects.all()

    def get(self, request, id):
        user = request.user
        task = ToDoTask.objects.get(user=user, id=id)
        task.delete()
        return redirect('list_of_tasks')


class TaskReorderView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        option = data.get('option')
        user = request.user

        if option == 'completed':
            tasks = ToDoTask.objects.filter(user=user, is_completed=True).order_by('created_date')
            if tasks.count() == 0:
                pass
            else:
                return render(request, 'task_list.html', {'tasks': tasks, 'count': tasks.count})
        elif option == 'priority':
            tasks = ToDoTask.objects.filter(user=user).order_by('priority')
            if tasks.count() == 0:
                pass
            else:
                return render(request, 'task_list.html', {'tasks': tasks, 'count': tasks.count})
        elif option == 'created_date':
            tasks = ToDoTask.objects.filter(user=user).order_by('created_date')
            if tasks.count() == 0:
                pass
            else:
                return render(request, 'task_list.html', {'tasks': tasks, 'count': tasks.count})
        elif option == 'updated_date':
            tasks = ToDoTask.objects.filter(user=user).order_by('update_date')
            if tasks.count() == 0:
                pass
            else:
                return render(request, 'task_list.html', {'tasks': tasks, 'count': tasks.count})

        tasks = ToDoTask.objects.filter(user=user)
        return render(request, 'task_list.html', {'tasks': tasks, 'count': tasks.count})


class CompleteTask(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        user = request.user

        task = ToDoTask.objects.get(user=user, id=id)
        task.is_completed = True
        task.save(update_fields=['is_completed'])

        return redirect('list_of_tasks')
