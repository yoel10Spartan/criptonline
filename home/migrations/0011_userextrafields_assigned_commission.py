# Generated by Django 4.0.2 on 2022-03-24 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_userextrafields_updated_vip'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextrafields',
            name='assigned_commission',
            field=models.BooleanField(default=False),
        ),
    ]
