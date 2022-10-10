import datetime

from django.db import models
from todoapp.todoapp_users.models import User
from django.utils.timezone import now


# Create your models here.
class ToDoTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    is_completed = models.BooleanField(default=False)

    class Priority(models.TextChoices):
        VERY_HIGH = 'Very High', 'Very High'
        HIGH = 'High', 'high'
        NORMAL = 'Normal', 'normal'
        LOW = 'Low', 'low'
        VERY_LOW = 'Very Low', 'very low'

    priority = models.CharField('Priority', max_length=50, choices=Priority.choices, blank=False,
                                default=Priority.NORMAL)
    created_date = models.DateTimeField(
        auto_now_add=True)  # auto now add only takes the time on the creation of the object
    update_date = models.DateTimeField(
        auto_now=True)  # auto now means that each time a save() method is called in ToDOTask model, this is updated

    def __str__(self):
        if self.is_completed is False:
            return f'Task {self.title} with priority {self.priority} is not completed yet.'
        else:
            return f'Task {self.title} with priority {self.priority} is completed.'
