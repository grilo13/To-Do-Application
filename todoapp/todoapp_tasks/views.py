from django.shortcuts import render

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
    permission_classes = (AllowAny,)
    queryset = ToDoTask.objects.all()

    def get(self, request):
        # user = request.user
        user = User.objects.get(id=2)
        tasks = user.tasks.all()
        serializer = self.serializer_class(tasks, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        data = request.data

        task = ToDoTask.objects.create(**data)

        user = User.objects.get(id=2)
        user.tasks.add(task)

        user.save()

        return Response(status=HTTP_200_OK)


class GetTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)
    queryset = ToDoTask.objects.all()

    def get(self, request, id):
        user = User.objects.get(id=2)
        task = user.tasks.filter(id=id).first()
        serializer = self.serializer_class(task)

        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, id):
        print(f'put')
        data = request.data
        task_description = data.get('description')
        user = User.objects.get(id=2)
        task = user.tasks.filter(id=id).first()
        task.description = task_description
        task.save(update_fields=['description'])

        return Response(status=HTTP_200_OK)

    def delete(self, request, id):
        data = request.data
        print(data)
        user = User.objects.get(id=2)
        task = user.tasks.filter(id=id).first()
        task.delete()
        return Response(status=HTTP_200_OK)
