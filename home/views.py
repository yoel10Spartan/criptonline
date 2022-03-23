import random
from datetime import date
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status, viewsets
from twilio.rest import Client
from center.models import Points
from center.views import PointsRequest
from task.models import Commissions
from users.models import User

from .models import VIP, CodeVerification, DataToAccept, InvitationCode
from .serializers import CodeVerificationSerializer, DataToAcceptSerializer, InvitationCodeSerializer, VIPListSerializer
from .models import UserExtraFields
from . import keys
from utils.date import Date

def get_random_num():
    return random.randint(10, 99)

class VerificationCodeRequest(viewsets.ModelViewSet):
    queryset = CodeVerification.objects.filter(is_active=True)
    serializer_class = CodeVerificationSerializer

    @action(detail=False, methods=['post'])
    def check_code(self, request):
        id_user = request.data['id_user']
        code = request.data['code_verification']
    
        code_verification = CodeVerification.objects.filter(
            id_user=id_user, code_verification=code
        ).exists()

        if code_verification:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def send_code(self, request):
        code_verification = '{}{}{}{}'.format(*[get_random_num() for _ in range(4)])
        id_user = '{}{}'.format(*[get_random_num() for _ in range(2)])
    
        client = Client(keys.account_sid, keys.auth_token)
        client.messages.create(
            body='Codigo de Criptoline {}'.format(code_verification),
            from_=keys.twilio_number,
            to=request.data['number_phone']
        )
        
        CodeVerification.objects.create(
            id_user=id_user, 
            code_verification=code_verification
        )

        return Response(
            {'id_user': id_user}, status=status.HTTP_200_OK
        )

class InvitationCodeRequest(viewsets.ModelViewSet):
    queryset = InvitationCode.objects.filter(is_active=True)
    serializer_class = InvitationCodeSerializer

    @action(detail=False, methods=['get'])
    def get_link_code(self, request):
        user = request.user
        user_extra_fields = UserExtraFields.objects.filter(user=user)
        code = str(user_extra_fields.first().code if user_extra_fields else '')
        link_code = 'https://{}/?code={}'.format(get_current_site(request).domain, code)
        return Response(
            {'link_code': link_code, 'invitation_code': code}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def validate_code(self, request):
        code = request.data['code']
        invitation_code = InvitationCode.objects.filter(code=code).first()
        user_extra_fields = UserExtraFields.objects 
        inviting_user = user_extra_fields.filter(code=invitation_code.id)
        
        user_extra_fields_self = user_extra_fields.filter(user=request.user)

        if(
            inviting_user.first().user.id != request.user.id
            and
            (not user_extra_fields_self.first().invitation_code)
        ):
            user_extra_fields_self.update(invitation_code=invitation_code)  
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            { "detail": "You can't invite yourself" }, 
            status=status.HTTP_409_CONFLICT,
        )

    @action(detail=False, methods=['get'])
    def get_all_code_request(self, request):
        user_extra_fields = UserExtraFields.objects 
        inviting_user = user_extra_fields.filter(user=request.user).first()
        
        if not inviting_user.invitation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        id_invitation_code = inviting_user.invitation_code.id
        print(id_invitation_code)
        user_inviting = user_extra_fields.filter(code=id_invitation_code).first()
    
        content = {
            'user_inviting': user_inviting.user.name,
        }
        return Response(content, status=status.HTTP_200_OK)

class VIPRequest(viewsets.ModelViewSet):
    queryset = VIP.objects.filter(is_active=True)
    serializer_class = VIPListSerializer

    def update_days_vip(self, request):
        user_extra_fields = UserExtraFields.objects.filter(user=request.user)
        user = user_extra_fields.first()
        
        if not user.vip: return 0
        
        days_vip_expiration = user.vip.expiration
        hiring_date_vip = user.updated_vip
        
        date_calc = Date(str(hiring_date_vip))
        day_passed = date_calc.days_passed()
         
        if day_passed >= days_vip_expiration:
            user_extra_fields.update(vip=None, updated_vip=date.today())
        
        return (days_vip_expiration - day_passed)
            
    @action(detail=False, methods=['get'])
    def get_vips(self, request):
        vip_list = VIP.objects.all()
        vip_serializer = VIPListSerializer(vip_list, many=True)
        return Response(vip_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_all_vip_request(self, request):
        
        user_extra_fields = UserExtraFields.objects.filter(user=request.user).first()
        vip_user_extra_fields = user_extra_fields.vip if user_extra_fields else False
        accept = bool(vip_user_extra_fields)

        data_to_accept = DataToAccept.objects.filter(user=request.user, is_active=True).first()
        vip_data_accept = data_to_accept.vip if data_to_accept else False
        hold = bool(vip_data_accept)

        select_vip_item = vip_data_accept or vip_user_extra_fields
        vip_select = select_vip_item if select_vip_item else None
        
        vip_serializer = VIPListSerializer(vip_select)

        exists = bool(vip_select)
        
        remaining_days = self.update_days_vip(request)

        return Response(
            {
                'accept': accept, 
                'hold': hold, 
                'vip_select': vip_serializer.data, 
                'exists': exists,
                'remaining_days': remaining_days
            },
            status=status.HTTP_200_OK
        )
        
    @action(detail=True, methods=['get'])
    def send_to_hold(self, request, pk=None):
        vip = VIP.objects.filter(pk=pk).first()
        user = request.user
        data_to_accept = DataToAccept.objects.filter(user=user)
        
        if vip:
            if data_to_accept.exists():
                data_to_accept.update(vip=vip)
            else:
                DataToAccept.objects.create(user=user, vip=vip)
            return Response(status=status.HTTP_204_NO_CONTENT) 
        return Response(
            {'detail':'invalid code'}, 
            status=status.HTTP_406_NOT_ACCEPTABLE
        )

    @action(detail=False, methods=['delete'])
    def reset_vip(self, request):
        user_extra_fields = UserExtraFields.objects.filter(user=request.user)
        data_to_accept = DataToAccept.objects.filter(user=request.user)

        if user_extra_fields.exists(): user_extra_fields.update(vip=None)
        if data_to_accept.exists(): 
            data_to_accept.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': 'You have to choose a vip'}, status=status.HTTP_406_NOT_ACCEPTABLE
        )
        
class DataToAcceptRequest(viewsets.ModelViewSet):
    queryset = DataToAccept.objects.filter(is_active=True)
    serializer_class = DataToAcceptSerializer
    
    @action(detail=False, methods=['get'])
    def get_users_by_accept(self, request):
        serialized = self.serializer_class(
            self.queryset.filter(is_active=True), 
            many=True
        )
        return Response(
            {'users': serialized.data}, 
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['put'])
    def accept_user(self, request, pk):
        data_to_accept = self.queryset.filter(pk=pk)
        
        if not data_to_accept.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user = data_to_accept.first().user
        vip = data_to_accept.first().vip
        user_extra_fields = UserExtraFields.objects.filter(user=user)
        
        user_extra_fields.update(vip=vip, updated_vip=date.today())
        data_to_accept.update(is_active=False)
        
        PointsRequest(user).update_or_create(vip)
        Commissions.objects.filter(user=request.user).update(
            remaining_withdrawals=vip.withdrawals
        )
        
        return Response(status=status.HTTP_204_NO_CONTENT)