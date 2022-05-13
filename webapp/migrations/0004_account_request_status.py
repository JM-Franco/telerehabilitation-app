# Generated by Django 4.0.3 on 2022-04-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_account_groups_account_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='account_request',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('denied', 'Denied')], default='pending', max_length=8),
        ),
    ]