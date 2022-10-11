from rest_framework import serializers
from .models import ToDoTask


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoTask
        fields = ['title',
                  'description',
                  'priority']

    def create(self, validated_data):
        print('validated data {0}'.format(validated_data))
        task = ToDoTask(
            **validated_data
        )
        task.save()
        return task
