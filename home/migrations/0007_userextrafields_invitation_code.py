# Generated by Django 4.0.2 on 2022-03-07 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_datatoaccept_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextrafields',
            name='invitation_code',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
