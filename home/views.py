from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status, viewsets

from .models import VIP, DataToAccept, InvitationCode
from .serializers import InvitationCodeSerializer, VIPListSerializer
from .models import UserExtraFields

class InvitationCodeRequest(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = InvitationCode.objects.filter(is_active=True)
    serializer_class = InvitationCodeSerializer

    @action(detail=False, methods=['get'])
    def get_link_code(self, request):
        user = request.user
        user_extra_fields = UserExtraFields.objects.filter(user=user)
        code = str(user_extra_fields.first().code)
        link_code = 'http://{}/?code={}'.format(get_current_site(request).domain, code)
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
            user_extra_fields_self.update(invitation_code=code)
            content = {
                'user_inviting': str(inviting_user.first().user),
            }
            return Response(content, status=status.HTTP_200_OK)

        return Response(
            { "detail": "You can't invite yourself" }, 
            status=status.HTTP_409_CONFLICT,
        )

class ValidateInvitationCode(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, code, format=None):
        
        invitation_code = InvitationCode.objects.filter(code=code).first()
        inviting_user = UserExtraFields.objects.filter(code=invitation_code.id).first()

        if inviting_user.user.id != request.user.id:
            content = {
                'user_inviting': str(inviting_user.user),
                'code': str(code),
            }
            return Response(content, status=status.HTTP_200_OK)

        return Response(
            { "detail": "You can't invite yourself" }, 
            status=status.HTTP_409_CONFLICT,
        )

class VIPRequest(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = VIP.objects.filter(is_active=True)
    serializer_class = VIPListSerializer

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
        vip_select = select_vip_item.id if select_vip_item else None

        exists = bool(vip_select)

        return Response(
            {'accept': accept, 'hold': hold, 'vip_select': vip_select, 'exists': exists},
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