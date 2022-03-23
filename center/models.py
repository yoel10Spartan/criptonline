from django.db import models
from users.models import User

class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_balance = models.BigIntegerField(default=0, null=True)
    total_benefit = models.BigIntegerField(default=0, null=True)
    frozen_quantity = models.BigIntegerField(default=0, null=True)
    day_benefit = models.BigIntegerField(default=0, null=True)
    expiration_time = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.user)
    
class PointsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    points_day = models.CharField(max_length=255, default=0)
    date_add = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.user)
    
class BankAccounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    name_bank = models.CharField(max_length=100, default='Nequi')
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.account_number)
    
class WithdrawalCurrent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    full_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)
    name_bank = models.CharField(max_length=100, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.user)
    
class WithdrawalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    withdrawal_current = models.ManyToManyField(WithdrawalCurrent)
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.user)