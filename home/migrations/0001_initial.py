# Generated by Django 4.0.2 on 2022-03-15 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.CharField(max_length=255)),
                ('code_verification', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvitationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_name', models.CharField(max_length=50)),
                ('expiration', models.IntegerField()),
                ('price', models.IntegerField()),
                ('withdrawals', models.IntegerField(default=0)),
                ('points_default', models.IntegerField(default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserExtraFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_requests_code', to='home.invitationcode')),
                ('invitation_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_requests_invitation_code', to='home.invitationcode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.vip')),
            ],
        ),
        migrations.CreateModel(
            name='DataToAccept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.vip')),
            ],
        ),
    ]
