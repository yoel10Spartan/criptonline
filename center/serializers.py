from .models import Points
from rest_framework import serializers

class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Points
        exclude = ('user', 'is_active', 'id',)