from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import InvitationCodeRequest, VIPRequest, ValidateInvitationCode

router = SimpleRouter()
router.register(r'vip', VIPRequest)
router.register(r'invitation_code', InvitationCodeRequest)

urlpatterns = [
    # path('validate_code_invitation/<str:code>/', ValidateInvitationCode.as_view(), name='code'),
    path('', include(router.urls))
]