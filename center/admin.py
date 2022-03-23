from django.contrib import admin

from .models import Points, BankAccounts, PointsHistory, WithdrawalCurrent, WithdrawalHistory

admin.site.register(Points)
admin.site.register(PointsHistory)
admin.site.register(BankAccounts)
admin.site.register(WithdrawalCurrent)
admin.site.register(WithdrawalHistory)