from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import PointsCenterRequest

router = SimpleRouter()
router.register(r'points', PointsCenterRequest)

urlpatterns = [
    path('', include(router.urls))
]