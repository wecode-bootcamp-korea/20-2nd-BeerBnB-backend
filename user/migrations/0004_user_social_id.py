# Generated by Django 3.2.3 on 2021-05-31 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_is_auth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='social_id',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
    ]
