from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (
    TaskRequest
)

router = SimpleRouter()
router.register(r'task', TaskRequest)

urlpatterns = [
    path('', include(router.urls))
]