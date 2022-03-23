from django.contrib import admin
from .models import AssignedTasks, Commissions, Task, TaskAmount, TaskHistory 

admin.site.register(Task)
admin.site.register(Commissions)
admin.site.register(AssignedTasks)
admin.site.register(TaskHistory)
admin.site.register(TaskAmount)