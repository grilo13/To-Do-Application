from django.shortcuts import render, redirect
from rest_framework.views import APIView

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

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
        tasks = user.tasks.all()
        context = {'tasks': tasks, 'count': tasks.count()}
        return render(request, 'task_list.html', context)


class CreateTask(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ToDoTask.objects.all()

    def post(self, request):
        user = request.user
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

        user.tasks.add(serializer.data.get('id'))
        user.save()

        return redirect('list_of_tasks')


class GetTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ToDoTask.objects.all()

    def get(self, request, id):
        user = request.user
        task = user.tasks.filter(id=id).first()
        context = {'task': task}
        return render(request, 'task_object.html', context)

    def put(self, request, id):
        print(f'put')
        data = request.data
        task_description = data.get('description')
        user = User.objects.get(id=2)
        task = user.tasks.filter(id=id).first()
        task.description = task_description
        task.save(update_fields=['description'])

        return Response(status=HTTP_200_OK)


class DeleteTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ToDoTask.objects.all()

    def get(self, request, id):
        user = request.user
        task = user.tasks.filter(id=id).first()
        task.delete()
        return redirect('list_of_tasks')


class TaskReorderView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        option = data.get('option')
        user = request.user

        if option == 'completed':
            tasks = user.tasks.filter(is_completed=True).order_by('created_date')
            if tasks.count() == 0:
                pass
            else:
                return render(request, 'task_list.html', {'tasks': tasks, 'count': tasks.count})

        tasks = user.tasks.all()
        return render(request, 'task_list.html', {'tasks': tasks, 'count': tasks.count})


class CompleteTask(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        user = request.user

        task = user.tasks.get(id=id)
        task.is_completed = True
        task.save(update_fields=['is_completed'])

        return redirect('list_of_tasks')
