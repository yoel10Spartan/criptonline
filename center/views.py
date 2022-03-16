import random
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework import request

from center.models import Points
from center.serializers import PointsSerializer
from center.models import Points

class PointsCenterRequest(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Points.objects.filter(is_active=True)
    serializer_class = PointsSerializer

    @action(detail=False, methods=['get'])
    def get_points_data(self, request):
        points = self.queryset.filter(user=request.user).first()
        points_serializer = self.serializer_class(points)
        return Response(points_serializer.data, status=status.HTTP_200_OK)

class PointsRequest():
    def __init__(self, user) -> None:
        self.queryset = Points.objects.filter(is_active=True)
        self.user = user
        self.filter_for_user = self.queryset.filter(user=self.user)
        
    def create(self):
        Points.objects.create(user=self.user)
        
    def update_or_create(self, vip_reference):
        if self.filter_for_user.exists():
            frozen_quantity = self.filter_for_user.first().frozen_quantity
            self.filter_for_user.update(
                frozen_quantity=(frozen_quantity + vip_reference.points_default),
                expiration_time=vip_reference.expiration,
            )
            return True
        Points.objects.create(
            user=self.user,
            frozen_quantity=vip_reference.points_default,
            expiration_time=vip_reference.expiration,
        )
        return True
    
    def update_day_benefit(self, points_add: int):
        points = self.filter_for_user.first().day_benefit
        self.filter_for_user.update(day_benefit=(points + points_add))
        return True
    
    @property
    def reset_day_benefit(self):
        self.filter_for_user.update(day_benefit=0)
        return True
    
    def update_available_balance(self, points_add: int):
        points = self.filter_for_user.first().available_balance
        self.filter_for_user.update(available_balance=(points + points_add))
        return True
        
    def update_total_benefit(self, points_add: int):
        points = self.filter_for_user.first().total_benefit
        self.filter_for_user.update(total_benefit=(points + points_add))
        return True
    
    def upgrade_all_benefits(self, points: int):
        self.update_day_benefit(points_add=points)
        self.update_available_balance(points_add=points)
        self.update_total_benefit(points_add=points)