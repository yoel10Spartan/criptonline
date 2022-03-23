from .models import BankAccounts, Points, PointsHistory, WithdrawalCurrent, WithdrawalHistory
from rest_framework import serializers
from datetime import datetime

class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Points
        exclude = ('user', 'is_active', 'id',)
        
class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = ('id', 'full_name', 'account_number', 'name_bank',)
        
class WithdrawalCurrentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WithdrawalCurrent
        fields = (
            'id', 
            'amount', 
            'date', 
            'full_name',
            'account_number',
            'name_bank',
        )
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        date = str(datetime.fromisoformat(ret['date'])).split('.')[0]
        ret['date'] = date
        return ret
        
class WithdrawalHistorySerializer(serializers.ModelSerializer):
    withdrawal_current = WithdrawalCurrentSerializer
    
    class Meta:
        model = WithdrawalHistory
        fields = ('id', 'withdrawal_current',)
        
class PointsHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PointsHistory
        fields = ('id', 'date_add', 'points_day', )