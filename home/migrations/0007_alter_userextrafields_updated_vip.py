# Generated by Django 4.0.2 on 2022-03-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_userextrafields_updated_vip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextrafields',
            name='updated_vip',
            field=models.DateField(auto_now_add=True),
        ),
    ]