from django.db import models
from users.models import User
from django.utils.timezone import now

class Task(models.Model):
    image = models.ImageField(upload_to='')
    title = models.CharField(max_length=100)
    points = models.BigIntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

class TaskHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task, through='TaskAmount')
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return "{}'s history".format(self.user.name)
    
class TaskAmount(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    task_history = models.ForeignKey(TaskHistory, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(self.task)

class Commissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personal_commission = models.BigIntegerField(null=True)
    completed_tasks = models.IntegerField(default=0)
    remaining_withdrawals = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.user)

class AssignedTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task)
    update_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.user)