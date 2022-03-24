import uuid

from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from center.views import PointsRequest

from home.models import InvitationCode, UserExtraFields
from task.models import Commissions
from .serializers import UserLoginSerializer, UserModelSerializer, UserSerializer, UserSignUpSerializer

class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })

@method_decorator(csrf_protect, name='dispatch')
class GetInformationUser(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        user = self.request.user
        print(user)

        isAuthenticated = user.is_authenticated

        user_serializer = UserSerializer(user)

        if isAuthenticated:
            return Response({
                'user': user_serializer.data, 
                'isAuthenticated': True 
            })

        return Response({ 'isAuthenticated': False })

@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):

        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        login(request, user)
        
        code = InvitationCode.objects.create(code=uuid.uuid1().hex)
        user_additional = UserExtraFields(user=user, code=code)
        user_additional.save()
        Commissions.objects.create(user=user)
        
        PointsRequest.create(user)

        return Response({ 'user': data }, status=status.HTTP_201_CREATED)

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        """User Sign In"""

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        
        return Response({ 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
      
class LogoutView(APIView):
    def get(self, request, format=None):
        try:
            logout(request)
            return Response({ 'success': 'Loggout Out' })
        except:
            return Response({ 'error': 'Something went wrong when logging out' })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': 'CSRF cookie set' })

class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user

        try:
            User.objects.filter(id=user.id).delete()

            return Response({ 'success': 'User deleted successfully' })
        except:
            return Response({ 'error': 'Something went wrong when trying to delete user' })
