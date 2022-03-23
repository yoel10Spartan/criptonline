from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import BankAccountsCenter, PointsCenterRequest, PointsHistoryCenter, WithdrawalCurrentCenter, WithdrawalHistoryCenter

router = SimpleRouter()
router.register(r'points', PointsCenterRequest)
router.register(r'bank_accounts', BankAccountsCenter)
router.register(r'withdrawal_history', WithdrawalHistoryCenter)
router.register(r'withdrawal_current', WithdrawalCurrentCenter)
router.register(r'points_history', PointsHistoryCenter)

urlpatterns = [
    path('', include(router.urls))
]