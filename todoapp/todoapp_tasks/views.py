from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

# Response
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

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
        serializer = self.serializer_class(tasks, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
