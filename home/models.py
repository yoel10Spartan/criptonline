from django.db import models

from users.models import User

class VIP(models.Model):
    vip_name = models.CharField(max_length=50, null=False)
    expiration = models.IntegerField()
    price = models.IntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.vip_name

class InvitationCode(models.Model):
    code = models.CharField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.code)

class UserExtraFields(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vip = models.ForeignKey(VIP, on_delete=models.CASCADE, null=True, blank=True)
    code = models.ForeignKey(InvitationCode, on_delete=models.CASCADE)
    invitation_code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '{} {}'.format(self.user.name, self.user.last_name)

class DataToAccept(models.Model):
    vip = models.ForeignKey(VIP, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)