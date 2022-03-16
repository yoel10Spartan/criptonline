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