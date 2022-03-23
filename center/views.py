import random
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework import request

from center.models import BankAccounts, Points, PointsHistory, WithdrawalCurrent, WithdrawalHistory
from center.serializers import BankAccountsSerializer, PointsHistorySerializer, PointsSerializer, WithdrawalCurrentSerializer, WithdrawalHistorySerializer
from center.models import Points
from task.models import Commissions
from rest_framework import exceptions

class PointsRequest():
    def __init__(self, user) -> None:
        self.queryset = Points.objects.filter(is_active=True)
        self.user = user
        self.filter_for_user = self.queryset.filter(user=self.user)
        self.available_balance_user = self.filter_for_user.first().available_balance
        self.day_benefit_total = self.filter_for_user.first().day_benefit
        
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
    
    def update_available_balance(self, points_add: int, action: str = 'more'):
        actions = {
            'more': (self.available_balance_user + points_add),
            'less': (self.available_balance_user - points_add)
        }
        self.filter_for_user.update(available_balance=actions[action])
        return True
    
    def get_available_balance(self):
        return self.available_balance_user
        
    def update_total_benefit(self, points_add: int):
        points = self.filter_for_user.first().total_benefit
        self.filter_for_user.update(total_benefit=(points + points_add))
        return True
    
    def upgrade_all_benefits(self, points: int):
        self.update_day_benefit(points_add=points)
        self.update_available_balance(points_add=points)
        self.update_total_benefit(points_add=points)
        
    def get(self):
        return self.filter_for_user.first()

class PointsCenterRequest(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Points.objects.filter(is_active=True)
    serializer_class = PointsSerializer

    @action(detail=False, methods=['get'])
    def get_points_data(self, request):
        points = self.queryset.filter(user=request.user).first()
        points_serializer = self.serializer_class(points)
        return Response(points_serializer.data, status=status.HTTP_200_OK)

# ===========================================================================

class PointsHistoryRequest:
    def __init__(self, user) -> None:
        self.user = user
    
    def add(self, points: str):
        PointsHistory.objects.create(
            points_day=points, user=self.user
        )
        
class PointsHistoryCenter(viewsets.ModelViewSet):
    queryset = PointsHistory.objects.all()
    serializer_class = PointsHistorySerializer

    @action(detail=False, methods=['get'])
    def get_items(self, request):
        points = PointsHistory.objects.filter(user=request.user)
        points_serializer = self.serializer_class(points, many=True)
        return Response(points_serializer.data, status=status.HTTP_200_OK)
        
# ===========================================================================

class WithdrawalHistoryRequest:
    def __init__(self, user) -> None:
        self.queryset = WithdrawalHistory.objects.filter(is_active=True)
        self.user = user
        self.filter_for_user = self.queryset.filter(user=self.user)
        self.withdrawal_history = WithdrawalHistory.objects
  
    @property
    def create(self):
        self.withdrawal_history.create(user=self.user)
        return
    
    def add_withdrawal(self, withdrawal_current: WithdrawalCurrent):
        withdrawal = self.filter_for_user.first()
        withdrawal.withdrawal_current.add(withdrawal_current)
        withdrawal.save()
        return
    
    def get(self):
        return self.filter_for_user.first().withdrawal_current.all()
    
    @property
    def get_withdrawal_serializer(self):
        return WithdrawalCurrentSerializer(self.get(), many=True).data
    
    @property
    def exists(self):
        return self.filter_for_user.exists()
  
class WithdrawalHistoryCenter(viewsets.ModelViewSet):
    queryset = WithdrawalHistory.objects.filter(is_active=True)
    serializer_class = WithdrawalHistorySerializer

    @action(detail=False, methods=['get'])
    def get_item(self, request):
        withdrawal_history_request = WithdrawalHistoryRequest(request.user)
        return Response(
            withdrawal_history_request.get_withdrawal_serializer, 
            status=status.HTTP_200_OK
        )
    
# ===========================================================================

class BankAccountsRequest:
    def __init__(self, user) -> None:
        self.queryset = BankAccounts.objects.filter(is_active=True)
        self.user = user
        self.filter_for_user = self.queryset.filter(user=self.user)
        self.bank_accounts = BankAccounts.objects
        self.serializer = BankAccountsSerializer
        
    def create(self, full_name: str, account_number: int, name_bank: str='Nequi'):
        self.bank_accounts.create(
            user=self.user,
            full_name=full_name,
            account_number=account_number,
            name_bank=name_bank
        )
        return
    
    def update(self, full_name: str, account_number: int, name_bank: str='Nequi'):
        self.filter_for_user.update(
            full_name=full_name,
            account_number=account_number,
            name_bank=name_bank
        )
        return
    
    def get_serializer(self):
        return self.serializer(self.filter_for_user.first()).data
    
    def get_object(self):
        return self.filter_for_user.first()
    
    @property
    def exists(self):
        return self.filter_for_user.exists()
    
class BankAccountsCenter(viewsets.ModelViewSet):
    queryset = BankAccounts.objects.filter(is_active=True)
    serializer_class = BankAccountsSerializer

    @action(detail=False, methods=['post', 'put'])
    def update_or_create(self, request):
        bank_accounts_request = BankAccountsRequest(request.user)
        full_name = request.data['full_name']
        account_number = request.data['account_number']
        name_bank = request.data['name_bank']
        
        if not bank_accounts_request.exists:
            bank_accounts_request.create(full_name, account_number, name_bank)
        else:
            bank_accounts_request.update(full_name, account_number, name_bank)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def get_items(self, request):
        bank_accounts_request = BankAccountsRequest(request.user)
        return Response(
            bank_accounts_request.get_serializer(), 
            status=status.HTTP_200_OK
        )

# ===========================================================================
    
class WithdrawalCurrentRequest:
    def __init__(self, user) -> None:
        self.queryset = WithdrawalCurrent.objects.filter(is_active=True)
        self.user = user
        self.filter_for_user = self.queryset.filter(user=self.user)
        self.withdrawal_current = WithdrawalCurrent.objects
        
    def create_item(self, request, amount: int, bank_account):
        withdrawal_current = WithdrawalCurrent(
            user=self.user, 
            amount=amount,
            full_name=bank_account.full_name,
            account_number=bank_account.account_number,
            name_bank=bank_account.name_bank,
        )
        
        commisions_user = Commissions.objects.filter(user=request.user).first()
        remaining_withdrawals = commisions_user.remaining_withdrawals
        
        if remaining_withdrawals <= 0:
            return
            
        withdrawal_current.save()
        return withdrawal_current
    
    def add_history(self, withdrawal_current: WithdrawalCurrent):
        withdrawal_user = WithdrawalHistoryRequest(self.user)
        if not withdrawal_user.exists: withdrawal_user.create
        
        withdrawal_user.add_withdrawal(withdrawal_current)
        return
    
class WithdrawalCurrentCenter(viewsets.ModelViewSet):
    queryset = WithdrawalCurrent.objects.filter(is_active=True)
    serializer_class = WithdrawalCurrentSerializer

    @action(detail=False, methods=['post'])
    def create_item(self, request):
        withdrawal_current_request = WithdrawalCurrentRequest(request.user)
        bank_accounts_request = BankAccountsRequest(request.user)
        points = PointsRequest(request.user)
        amount = int(request.data['amount'])
        
        if not (amount <= points.get_available_balance()):
            return Response(
                'Sin fondos suficientes', 
                status=status.HTTP_409_CONFLICT
            )
        
        bank_account = bank_accounts_request.get_object()
        
        if not bank_account:
            return Response(
                'Agrega una cuenta de banco', 
                status=status.HTTP_409_CONFLICT
            )
        
        withdrawal_current = withdrawal_current_request.create_item(
            request,
            amount=request.data['amount'],
            bank_account=bank_account
        )
        
        if not withdrawal_current:
            return Response(
                'No tienes retiros suficientes', 
                status=status.HTTP_409_CONFLICT
            )
        
        points.update_available_balance(points_add=amount, action='less')
        withdrawal_current_request.add_history(withdrawal_current)
        
        withdrawals = Commissions.objects.filter(user=request.user)
        withdrawals.update(
            remaining_withdrawals=(withdrawals.first().remaining_withdrawals - 1)
        )
        
        return Response(status=status.HTTP_204_NO_CONTENT)

# ===========================================================================