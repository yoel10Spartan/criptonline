from dataclasses import fields
from .models import VIP, InvitationCode
from rest_framework import serializers

class VIPListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VIP
        fields = [ 'id', 'vip_name', 'expiration', 'price' ]

class InvitationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCode
        fields = [ 'code', ]