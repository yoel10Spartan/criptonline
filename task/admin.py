from django.contrib import admin
from .models import AssignedTasks, Commissions, Task  

admin.site.register(Task)
admin.site.register(Commissions)
admin.site.register(AssignedTasks)