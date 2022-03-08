from django.contrib import admin

from home.models import VIP, DataToAccept, InvitationCode, UserExtraFields

admin.site.register(VIP)
admin.site.register(InvitationCode)
admin.site.register(UserExtraFields)
admin.site.register(DataToAccept)