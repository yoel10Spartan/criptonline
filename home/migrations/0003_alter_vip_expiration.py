# Generated by Django 4.0.2 on 2022-02-28 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_invitationcode_code_alter_vip_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vip',
            name='expiration',
            field=models.IntegerField(),
        ),
    ]
