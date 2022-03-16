from users.serializers import UserSerializer
from .models import VIP, CodeVerification, InvitationCode, DataToAccept
from rest_framework import serializers

class VIPListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VIP
        fields = ['id', 'vip_name', 'expiration', 'price']

class InvitationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCode
        fields = ['code',]

class CodeVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeVerification
        fields = ['id_user', 'code_verification']
        
class DataToAcceptSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    vip = VIPListSerializer()
    
    class Meta:
        model = DataToAccept
        exclude = ['is_active',]