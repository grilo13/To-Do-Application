from django.db import models


# Create your models here.
class ToDoTask(models.Model):
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

    def __str__(self):
        if self.is_completed is False:
            return f'Task {self.title} with priority {self.priority} is not completed yet.'
        else:
            return f'Task {self.title} with priority {self.priority} is completed.'