import random
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework import request

from center.models import Points
from center.views import PointsHistoryRequest, PointsRequest
from home.models import UserExtraFields
from .models import AssignedTasks, Commissions, Task, TaskAmount, TaskHistory
from .serializers import TaksSerializer
from utils.date import Date

class TaskRequest(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.filter(is_active=True)
    serializer_class = TaksSerializer

    assigned_taks = AssignedTasks.objects
    TOTAL_TASK = 5
    
    @staticmethod
    def verify_date(date: str):
        date_assigned = datetime.fromisoformat(date)
        now = datetime.now()
        tuple_bool = list(zip([now.day, now.month, now.year], [date_assigned.day, date_assigned.month, date_assigned.year]))
        return any([i>j for i,j in tuple_bool])
    
    def get_task_random(self):
        return random.sample(list(self.queryset), k=self.TOTAL_TASK)
    
    def update_or_create(self, request, is_exists: bool):
        list_task = self.get_task_random()
        if is_exists:
            assignedtask = self.assigned_taks.filter(user=request.user).first()
            assignedtask.tasks.clear()
        else:
            assignedtask = self.assigned_taks.create(user=request.user)
        assignedtask.tasks.add(*list_task)
        assignedtask.save()
        return list_task

    @action(detail=False, methods=['get'])
    def get_taks(self, request):
        task_assigned = self.assigned_taks.filter(user=request.user)
        list_task = []
        
        if not UserExtraFields.objects.filter(user=request.user).first().vip:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if not task_assigned.exists():
            list_task = self.update_or_create(request, task_assigned.exists())
            task_assigned.update(update_date=datetime.now())
            
        if Date(str(task_assigned.first().update_date)).verify_date():
            list_task = self.update_or_create(request, task_assigned.exists())
            
            points = PointsRequest(request.user)
            PointsHistoryRequest(request.user).add(points.day_benefit_total)
            points.reset_day_benefit
            
            Commissions.objects \
                .filter(user=request.user) \
                .update(completed_tasks=0, personal_commission=0)
            
            task_assigned.update(update_date=datetime.now())

        list_task = task_assigned.first().tasks

        task = TaksSerializer(list_task, many=True)
        return Response(task.data, status=status.HTTP_200_OK)

    def change_commissions(self, request: request, points: int, task_num: int):
        commissions = Commissions.objects
        commissions_for_user = commissions.filter(user=request.user)
        
        if commissions_for_user.exists():
            personal_commission = commissions_for_user.first().personal_commission
            completed_tasks = commissions_for_user.first().completed_tasks
            commissions_for_user.update(
                personal_commission=(personal_commission + points),
                completed_tasks=(completed_tasks + task_num)
            )
            return
        
        commissions.create(
            user=request.user,
            personal_commission=points,
            completed_tasks=task_num,
        )
        return

    def get_or_create_history_task(self, user):
        task_history = TaskHistory.objects.filter(user=user)
        if not task_history.exists():
            return TaskHistory.objects.create(user=user)
        return task_history.first()

    def add_history_task(self, request, task):
        task_history = self.get_or_create_history_task(request.user)
        TaskAmount.objects.create(task=task, task_history=task_history)
        return
    
    def get_history_task(self, request):
        task_history = self.get_or_create_history_task(request.user)
        tasks = TaskAmount.objects.filter(task_history=task_history)
        return [i.task for i in tasks]
    
    @action(detail=False, methods=['get'])
    def get_task_history(self, request):
        tasks = self.get_history_task(request)
        tasks_serializer = TaksSerializer(tasks, many=True)
        return Response(tasks_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def mark_complete(self, request, pk: int):
        task_assigned = self.assigned_taks.filter(user=request.user)
        tasks = task_assigned.first().tasks
        points = tasks.filter(id=pk).first().points

        tasks.remove(pk)
        
        if not tasks.filter(id=pk).exists():
            self.change_commissions(request, points=points, task_num=1)
            
            points_request = PointsRequest(request.user)
            points_request.upgrade_all_benefits(points=points)
            
            self.add_history_task(request, self.queryset.get(id=pk))
            
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def get_commision_data(self, request):
        commissions = Commissions.objects.get(user=request.user)
        total_assets = Points.objects.get(user=request.user).available_balance
        personal_commission = commissions.personal_commission
        completed_tasks = commissions.completed_tasks
        remaining_withdrawals = commissions.remaining_withdrawals
        
        return Response({
            'total_assets': total_assets, 
            'personal_commissions': personal_commission,
            'remaining_withdrawals': remaining_withdrawals,
            'completed_tasks': completed_tasks,
            'total_tasks': self.TOTAL_TASK
        },
            status=status.HTTP_200_OK
        )