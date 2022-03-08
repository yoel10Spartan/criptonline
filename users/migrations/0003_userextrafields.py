# Generated by Django 4.0.2 on 2022-03-05 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_vip_expiration'),
        ('users', '0002_remove_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtraFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.invitationcode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.vip')),
            ],
        ),
    ]
