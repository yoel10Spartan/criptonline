from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import InvitationCodeRequest, VIPRequest, get_code_verification, verification_code

router = SimpleRouter()
router.register(r'vip', VIPRequest)
router.register(r'invitation_code', InvitationCodeRequest)

urlpatterns = [
    path('code_verification/', get_code_verification),
    path('verification_code/', verification_code),
    path('', include(router.urls))
]