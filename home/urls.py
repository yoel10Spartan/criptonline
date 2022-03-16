from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (
    DataToAcceptRequest,
    InvitationCodeRequest, 
    VIPRequest, 
    VerificationCodeRequest
)

router = SimpleRouter()
router.register(r'vip', VIPRequest)
router.register(r'data_to_accept', DataToAcceptRequest)
router.register(r'invitation_code', InvitationCodeRequest)
router.register(r'verification_code', VerificationCodeRequest)

urlpatterns = [
    path('', include(router.urls))
]