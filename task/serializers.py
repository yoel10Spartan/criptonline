from rest_framework import serializers
from .models import Task, Commissions, AssignedTasks

class TaksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'image', 'title', 'points',]

class CommissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commissions
        fields = ['user', 'total_assets', 'personal_commission', 'completed_tasks', 'unused_withdrawals']

class AssignedTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedTasks
        fields = ['user', 'tasks', 'update_date']