# from django.contrib.sites.shortcuts import get_current_site
# from rest_framework.decorators import api_view, authentication_classes
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework import status, viewsets

# from users.models import User
# from users.serializers import UserSerializer

# class UserRequest(viewsets.ModelViewSet):
#     queryset = User.objects.filter(is_active=True)
#     serializer_class = UserSerializer

#     @action(detail=False, methods=['post'])
#     def get_all(self, request):
#         ...

#     @action(detail=False, methods=['post'])
#     def send_code(self, request):
#         ...