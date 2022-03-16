import random
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework import request

from center.models import Points
from center.views import PointsRequest
from home.models import UserExtraFields
from .models import AssignedTasks, Commissions, Task
from .serializers import TaksSerializer

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
        
        if(
            (not task_assigned.exists()) 
            or
            (TaskRequest.verify_date(str(task_assigned.first().update_date)))
        ):
            list_task = self.update_or_create(request, task_assigned.exists())
            
            PointsRequest(request.user).reset_day_benefit
            Commissions.objects \
                .filter(user=request.user) \
                .update(completed_tasks=0, personal_commission=0)
                
            task_assigned.update(update_date=datetime.now())
        else:
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
            
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def get_commision_data(self, request):
        commissions = Commissions.objects.get(user=request.user)
        total_assets = Points.objects.get(user=request.user).available_balance
        personal_commission = commissions.personal_commission
        completed_tasks = commissions.completed_tasks
        return Response({
            'total_assets': total_assets, 
            'personal_commissions': personal_commission,
            'remaining_withdrawals': 0,
            'completed_tasks': completed_tasks,
            'total_tasks': self.TOTAL_TASK
        },
            status=status.HTTP_200_OK
        )